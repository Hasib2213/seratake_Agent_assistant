# QMS Platform API Testing Guide

## Prerequisites
- Application running at `http://localhost:8000`
- Gemini API key configured
- PostgreSQL and Redis running

---

## 1. Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-16T10:30:00.123456",
  "version": "1.0.0"
}
```

---

## 2. AI Agents

### 2.1 Risk Prediction Agent
```bash
curl -X POST "http://localhost:8000/api/v1/agents/risk-prediction?org_id=org_123"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "status": "success",
    "agent": "RiskPredictionAgent",
    "org_id": "org_123",
    "analysis": {
      "status": "success",
      "total_incidents": 5,
      "categorized_data": {
        "Safety": [...]
      }
    },
    "predictions": {
      "status": "success",
      "predictions": "Risk prediction insights...",
      "timestamp": "2024-02-16T10:30:00.123456"
    }
  },
  "executed_at": "2024-02-16T10:30:00.123456"
}
```

---

### 2.2 Predictive Maintenance Agent
```bash
curl -X POST "http://localhost:8000/api/v1/agents/predictive-maintenance?org_id=org_123"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "status": "success",
    "agent": "PredictiveMaintenanceAgent",
    "org_id": "org_123",
    "equipment_data": {
      "status": "success",
      "equipment_count": 2,
      "equipment": [
        {
          "id": "eq_001",
          "name": "CNC Machine",
          "usage_hours": 450,
          "last_maintenance": "2024-01-01"
        }
      ]
    },
    "maintenance_schedule": {
      "status": "success",
      "maintenance_schedule": "Maintenance schedule recommendations..."
    }
  },
  "executed_at": "2024-02-16T10:30:00.123456"
}
```

---

### 2.3 Training Gap Analysis Agent
```bash
curl -X POST "http://localhost:8000/api/v1/agents/training-gaps?org_id=org_123"
```

---

### 2.4 Supplier Evaluation Agent
```bash
curl -X POST "http://localhost:8000/api/v1/agents/supplier-evaluation?org_id=org_123"
```

---

### 2.5 Root Cause Analysis Agent
```bash
curl -X POST "http://localhost:8000/api/v1/agents/root-cause-analysis?org_id=org_123"
```

---

### 2.6 Run All Agents
```bash
curl -X POST "http://localhost:8000/api/v1/agents/run-all?org_id=org_123"
```

---

## 3. Document Assistant

### 3.1 Summarize Document
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/document/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a comprehensive quality assurance procedure document that outlines all steps for inspection...",
    "max_length": 200
  }'
```

**Response:**
```json
{
  "status": "success",
  "summary": "Quality assurance procedure outlines inspection steps, requirements, and responsibilities...",
  "word_count": 45,
  "generated_at": "2024-02-16T10:30:00.123456"
}
```

### 3.2 Extract Key Points
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/document/key-points" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Document content here..."
  }'
```

### 3.3 Get Improvement Suggestions
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/document/improve" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Document content here..."
  }'
```

---

## 4. Sentiment Analysis Assistant

### 4.1 Analyze Single Feedback
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/sentiment/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "feedback": "Great product quality but delivery was slow. Would recommend with improvements on logistics."
  }'
```

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "overall_sentiment": "Neutral",
    "sentiment_score": 0.5,
    "key_topics": ["product quality", "delivery", "logistics"],
    "concerns": ["slow delivery", "logistics issues"],
    "compliments": ["great product quality"],
    "recommended_action": "Improve logistics and delivery processes"
  },
  "analyzed_at": "2024-02-16T10:30:00.123456"
}
```

### 4.2 Batch Sentiment Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/sentiment/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "feedback_list": [
      "Excellent service and fast delivery!",
      "Product broke after one week",
      "Average quality, acceptable price"
    ]
  }'
```

### 4.3 Identify Trends
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/sentiment/trends" \
  -H "Content-Type: application/json" \
  -d '{
    "feedback_list": [
      "Great product",
      "Slow delivery",
      "Poor customer support",
      "Good quality",
      "Expensive shipping"
    ]
  }'
```

---

## 5. Context Analysis Assistant

### 5.1 PESTEL Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/context/pestel" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Our manufacturing company operates in developing economies, facing regulatory changes in environmental standards, increased competition from Asian manufacturers, and growing consumer demand for sustainable products."
  }'
```

**Response:**
```json
{
  "status": "success",
  "pestel": {
    "political": [
      "Regulatory changes in environmental standards - HIGH impact",
      "Trade policy uncertainty - MEDIUM impact"
    ],
    "economic": [
      "Currency fluctuations in emerging markets - HIGH impact",
      "Rising labor costs - MEDIUM impact"
    ],
    "social": [
      "Growing sustainability demand - HIGH impact",
      "Workforce demographics change - MEDIUM impact"
    ],
    "technological": [
      "Industry 4.0 adoption - HIGH impact",
      "Automation opportunities - HIGH impact"
    ],
    "environmental": [
      "Carbon emission regulations - HIGH impact",
      "Resource scarcity - MEDIUM impact"
    ],
    "legal": [
      "Compliance requirements increase - HIGH impact",
      "Labor law changes - MEDIUM impact"
    ]
  },
  "analysis_date": "2024-02-16T10:30:00.123456"
}
```

### 5.2 SWOT Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/context/swot" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Mid-sized manufacturing company with 20 years experience, strong technical team, but aging equipment and limited digital capabilities."
  }'
```

### 5.3 TOWS Matrix
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/context/tows" \
  -H "Content-Type: application/json" \
  -d '{
    "swot_data": {
      "strengths": ["Experienced team", "Strong reputation", "Good supplier network"],
      "weaknesses": ["Aging equipment", "Limited IT capabilities", "High operational costs"],
      "opportunities": ["Industry 4.0 adoption", "Emerging markets", "Green product demand"],
      "threats": ["Asian competition", "Regulatory changes", "Supply chain disruption"]
    }
  }'
```

---

## 6. Compliance Assistant

### 6.1 Check ISO Compliance
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/compliance/check" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Quality Management System procedure document content...",
    "standard": "ISO 9001"
  }'
```

**Response:**
```json
{
  "status": "success",
  "compliance_check": {
    "clause_4": {
      "status": "Compliant",
      "details": "Adequate context analysis documented"
    },
    "clause_5": {
      "status": "Compliant",
      "details": "Leadership roles and responsibilities defined"
    },
    "clause_6": {
      "status": "Gap",
      "details": "Risk assessment methodology incomplete",
      "remediation": "Add risk assessment procedure with ISO 31000 alignment"
    },
    "clause_7": {
      "status": "Compliant",
      "details": "Support resources adequately documented"
    },
    "clause_8": {
      "status": "Gap",
      "details": "Supplier management controls insufficient",
      "remediation": "Implement supplier performance evaluation system"
    }
  },
  "standard": "ISO 9001",
  "checked_at": "2024-02-16T10:30:00.123456"
}
```

### 6.2 Identify Compliance Gaps
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/compliance/gaps" \
  -H "Content-Type: application/json" \
  -d '{
    "current_state": "Current quality management system includes basic documentation, manual processes, and limited automation",
    "target_standard": "ISO 9001:2015"
  }'
```

---

## 7. Configuration Endpoints

### 7.1 Get ISO Clauses
```bash
curl -X GET "http://localhost:8000/api/v1/config/iso-clauses"
```

**Response:**
```json
{
  "status": "success",
  "iso_clauses": {
    "4": "Context of the Organization",
    "5": "Leadership",
    "6": "Planning",
    "7": "Support",
    "8": "Operation",
    "9": "Performance Evaluation",
    "10": "Improvement"
  }
}
```

### 7.2 Get RBAC Configuration
```bash
curl -X GET "http://localhost:8000/api/v1/config/rbac"
```

### 7.3 Get Features Status
```bash
curl -X GET "http://localhost:8000/api/v1/config/features"
```

---

## Testing with Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_risk_prediction():
    url = f"{BASE_URL}/api/v1/agents/risk-prediction"
    params = {"org_id": "org_123"}
    response = requests.post(url, params=params)
    print(json.dumps(response.json(), indent=2))

def test_document_summarize():
    url = f"{BASE_URL}/api/v1/assistant/document/summarize"
    data = {
        "content": "Your document here...",
        "max_length": 200
    }
    response = requests.post(url, json=data)
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_risk_prediction()
    test_document_summarize()
```

---

## Performance Metrics

Expected response times:
- Health check: < 100ms
- Document summarization: 2-5 seconds
- Risk prediction: 5-10 seconds
- Sentiment analysis: 1-3 seconds
- Batch operations: 10-30 seconds

---

## Error Handling

All errors follow this format:
```json
{
  "status": "error",
  "message": "Error description",
  "status_code": 500,
  "timestamp": "2024-02-16T10:30:00.123456"
}
```

Common errors:
- `400`: Bad request (invalid input)
- `401`: Unauthorized (missing API key)
- `429`: Rate limit exceeded
- `500`: Internal server error

---

## Debugging

Enable verbose logging:
```bash
# In .env
LOG_LEVEL=DEBUG
LANGCHAIN_VERBOSE=true
LANGCHAIN_DEBUG=true
```

View logs:
```bash
tail -f logs/qms.log
docker-compose logs -f api
```

---

**Last Updated:** February 2024