# QMS Platform - Production Deployment Guide

Complete guide for deploying QMS Platform to production with LangChain + Gemini.

---

## 📋 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database backups configured
- [ ] SSL certificates obtained
- [ ] API keys secured
- [ ] Monitoring setup
- [ ] Logging configured
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Database indices optimized
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation updated

---

## 🌍 Deployment Options

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker 20.10+
- Docker Compose 1.29+

**Deployment Steps:**

1. **Prepare Environment**
```bash
git clone <repo-url>
cd qms-project
cp .env.example .env
# Edit .env with production values
```

2. **Configure .env**
```env
ENVIRONMENT=production
DEBUG=false
GEMINI_API_KEY=your-production-key
DATABASE_URL=postgresql://user:pass@db-host:5432/qms_db
SECRET_KEY=generate-strong-random-key
ALLOWED_ORIGINS=https://yourdomain.com
```

3. **Start Services**
```bash
docker-compose -f docker-compose.yml up -d
docker-compose logs -f api
```

4. **Verify Deployment**
```bash
curl https://yourdomain.com/health
```

---

### Option 2: Kubernetes (Advanced)

**Prerequisites:**
- Kubernetes cluster (1.24+)
- kubectl configured
- Helm 3+

**Deployment Steps:**

1. **Create Namespace**
```bash
kubectl create namespace qms-prod
```

2. **Create Secrets**
```bash
kubectl create secret generic qms-secrets \
  --from-literal=gemini-api-key=your-key \
  --from-literal=db-password=your-password \
  -n qms-prod
```

3. **Deploy with Helm**
```bash
helm install qms ./helm-chart \
  --namespace qms-prod \
  --values values-prod.yaml
```

4. **Verify Pods**
```bash
kubectl get pods -n qms-prod
kubectl logs -f deployment/qms-api -n qms-prod
```

---

### Option 3: VPS/EC2 Deployment

**Prerequisites:**
- Ubuntu 22.04 LTS
- Python 3.11+
- Nginx
- PostgreSQL
- Redis

**Deployment Steps:**

1. **System Setup**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3-pip postgresql redis-server nginx

# Create application user
sudo useradd -m -d /home/qms qms
sudo su - qms
```

2. **Clone Repository**
```bash
cd /home/qms
git clone <repo-url> app
cd app
```

3. **Setup Python Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure Systemd Service**
```bash
sudo tee /etc/systemd/system/qms.service > /dev/null <<EOF
[Unit]
Description=QMS Platform
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=qms
WorkingDirectory=/home/qms/app
Environment="PATH=/home/qms/app/venv/bin"
ExecStart=/home/qms/app/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
EOF
```

5. **Enable and Start Service**
```bash
sudo systemctl enable qms
sudo systemctl start qms
sudo systemctl status qms
```

6. **Configure Nginx Reverse Proxy**
```bash
sudo tee /etc/nginx/sites-available/qms > /dev/null <<EOF
upstream qms_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://qms_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    location /static/ {
        alias /home/qms/app/static/;
        expires 30d;
    }
}
EOF
```

7. **Enable Nginx**
```bash
sudo ln -s /etc/nginx/sites-available/qms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔐 Security Hardening

### 1. Database Security
```sql
-- Create database user
CREATE USER qms_user WITH PASSWORD 'strong-random-password';
CREATE DATABASE qms_db OWNER qms_user;

-- Restrict permissions
GRANT CONNECT ON DATABASE qms_db TO qms_user;
GRANT USAGE ON SCHEMA public TO qms_user;
GRANT CREATE ON SCHEMA public TO qms_user;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
```

### 2. API Security
```python
# In config.py
ALLOWED_ORIGINS = ["https://yourdomain.com"]
ALLOW_CREDENTIALS = True
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_PERIOD = 60
```

### 3. SSL/TLS Certificate
```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly -d yourdomain.com
```

### 4. Firewall Rules
```bash
# UFW (Ubuntu)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 5. API Key Management
```bash
# Rotate Gemini API key regularly
# Store in secure vault (AWS Secrets Manager, HashiCorp Vault, etc.)
# Never commit to version control
```

---

## 📊 Monitoring & Observability

### 1. Application Monitoring
```bash
# Install Prometheus + Grafana
docker run -d -p 9090:9090 prom/prometheus
docker run -d -p 3000:3000 grafana/grafana
```

### 2. Logging
```yaml
# In docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "100m"
    max-file: "10"
    labels: "service=qms"
```

### 3. Error Tracking
```python
# Optional: Sentry integration
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://your-sentry-url",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1
)
```

---

## 🔄 Database Management

### Backups
```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/qms"
DB_NAME="qms_db"
DB_USER="qms_user"

mkdir -p $BACKUP_DIR
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/qms_$(date +%Y%m%d_%H%M%S).sql.gz

# Keep only 30 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

# Upload to S3
aws s3 sync $BACKUP_DIR s3://your-backup-bucket/
```

### Migrations
```bash
# Using Alembic for database versioning
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## 🚀 Performance Optimization

### 1. Database Optimization
```sql
-- Create indices
CREATE INDEX idx_org_risks ON risks(organization_id);
CREATE INDEX idx_doc_status ON documents(status);
CREATE INDEX idx_user_org ON users(organization_id);
ANALYZE;

-- Query optimization
VACUUM ANALYZE;
```

### 2. Caching Strategy
```python
# Redis caching
@app.get("/api/v1/config/iso-clauses")
async def get_iso_clauses():
    cache_key = "iso_clauses"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    result = ISO_CLAUSES
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return result
```

### 3. Connection Pooling
```python
# SQLAlchemy configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

---

## 🔍 Monitoring Checklist

- **Uptime**: Target 99.9%
- **Response Time**: < 500ms (p95)
- **Error Rate**: < 0.1%
- **API Latency**: Track by endpoint
- **Database**: Connection pool usage, slow queries
- **Memory**: Application and database memory usage
- **Disk**: Available space, backup storage
- **Network**: Bandwidth usage, DDoS detection

---

## 📈 Scaling Strategy

### Horizontal Scaling
```bash
# Load balancer (HAProxy or AWS ELB)
# Multiple API instances
docker-compose up -d --scale api=3
```

### Vertical Scaling
```bash
# Increase instance size
# Increase database resources
# Optimize database indices
```

### Caching Layer
```bash
# Redis for session/caching
# CDN for static files
# Database query caching
```

---

## 🚨 Incident Response

### Health Checks
```bash
# API health
curl https://yourdomain.com/health

# Database connectivity
psql -U qms_user -d qms_db -c "SELECT 1"

# Redis connectivity
redis-cli ping
```

### Common Issues

**Database Connection Failed:**
```bash
# Check database service
sudo systemctl status postgresql

# Check connection string
cat .env | grep DATABASE_URL

# Test connection
psql -c "SELECT version();"
```

**High Memory Usage:**
```bash
# Check logs
docker logs qms_api

# Restart service
docker-compose restart api

# Scale down agents
AGENTS_CONCURRENCY=2
```

**Slow API Response:**
```bash
# Check database slow query log
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC;

# Check Nginx logs
tail -f /var/log/nginx/error.log
```

---

## 📝 Maintenance Schedule

**Daily:**
- Monitor error rates
- Check backups completed
- Review error logs

**Weekly:**
- Database maintenance
- Security patches review
- Performance analysis

**Monthly:**
- Dependency updates
- Security audit
- Capacity planning

**Quarterly:**
- Database optimization
- Load testing
- Disaster recovery drill

---

## 🔐 Compliance & Security

- **ISO 27001**: Information Security Management
- **GDPR**: If handling EU data
- **SOC 2**: Security & availability
- **PCI DSS**: If handling payment data

---

## Support & Documentation

- **Runbook**: Operational procedures
- **API Docs**: http://yourdomain.com/docs
- **Status Page**: Real-time system status
- **Contact**: ops-team@yourdomain.com

---

## Post-Deployment Verification

```bash
# Check all services running
docker-compose ps

# Verify API endpoints
curl https://yourdomain.com/api/v1/config/features

# Test AI agents
curl -X POST https://yourdomain.com/api/v1/agents/risk-prediction?org_id=test

# Monitor logs
docker-compose logs -f api

# Performance test
ab -n 100 -c 10 https://yourdomain.com/health
```

---

**Last Updated:** February 2024  
**Version:** 1.0.0