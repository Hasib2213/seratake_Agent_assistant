# MongoDB Atlas Setup Guide

This guide will help you set up MongoDB Atlas for the QMS Platform.

## Prerequisites
- MongoDB Atlas account (free tier available)
- Python 3.8+

## Step 1: Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Try Free" and sign up
3. Verify your email address

## Step 2: Create a Cluster

1. After logging in, click "Build a Database"
2. Choose the **FREE** M0 cluster (Shared)
3. Select your preferred cloud provider and region (choose closest to you)
4. Click "Create Cluster" (this may take 3-5 minutes)

## Step 3: Configure Database Access

1. In the left sidebar, click "Database Access"
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and **strong password** (save these!)
5. Set user privileges to "Atlas Admin" (or "Read and write to any database")
6. Click "Add User"

## Step 4: Configure Network Access

1. In the left sidebar, click "Network Access"
2. Click "Add IP Address"
3. For development:
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - ⚠️ For production, use specific IP addresses
4. Click "Confirm"

## Step 5: Get Connection String

1. Go back to "Database" in the left sidebar
2. Click "Connect" button on your cluster
3. Choose "Connect your application"
4. Select:
   - Driver: **Python**
   - Version: **3.12 or later**
5. Copy the connection string (looks like):
   ```
   mongodb+srv://username:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

## Step 6: Configure Your Application

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and update:
   ```env
   MONGODB_URI=mongodb+srv://your_username:your_password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DB_NAME=qms_db
   ```

   Replace:
   - `your_username` with your MongoDB username
   - `your_password` with your MongoDB password
   - `cluster0.xxxxx` with your actual cluster address

## Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 8: Run the Application

```bash
python -m uvicorn main:app --reload
```

Or:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Verify Connection

When the application starts, you should see:
```
INFO - Connecting to MongoDB Atlas...
INFO - Successfully connected to MongoDB Atlas - Database: qms_db
INFO - Creating database indexes...
INFO - Database indexes created successfully
```

## MongoDB Collections

The following collections will be automatically created:
- `users` - User accounts
- `organizations` - Company/organization data
- `documents` - Document management
- `risks` - Risk register
- `policies` - Quality policies
- `suppliers` - Supplier/vendor management
- `equipment` - Equipment/asset tracking
- `non_conformities` - Non-conformity reports (CAPA)
- `training` - Training records
- `audits` - Audit records
- `kpis` - Key performance indicators
- `notifications` - User notifications
- `ai_agent_logs` - AI agent execution logs
- `customer_feedback` - Customer feedback & sentiment

## Indexes

The application automatically creates indexes for:
- Email and username (unique)
- Organization IDs
- Status fields
- Risk scores
- Document types
- Performance optimization

## MongoDB Compass (Optional GUI)

You can use MongoDB Compass to visually browse your database:

1. Download [MongoDB Compass](https://www.mongodb.com/products/compass)
2. Use the same connection string from your `.env` file
3. Connect and explore your data

## Troubleshooting

### Connection Timeout
- Check if your IP address is whitelisted in Network Access
- Verify your username and password are correct
- Check if your firewall allows outbound connections on port 27017

### Authentication Failed
- Double-check username and password
- Ensure special characters in password are URL encoded
  - Example: `p@ssw0rd` becomes `p%40ssw0rd`

### Database Not Created
- Databases in MongoDB are created automatically when first document is inserted
- Run the application and make your first API call

## Production Recommendations

1. **Network Access**: Use specific IP addresses instead of 0.0.0.0/0
2. **User Permissions**: Create separate users with minimal required permissions
3. **Backup**: Enable automated backups in Atlas
4. **Monitoring**: Set up alerts in MongoDB Atlas
5. **Connection Pool**: Configure appropriate pool size in `database.py`

## Support

- MongoDB Atlas Docs: https://docs.atlas.mongodb.com/
- MongoDB Python Driver: https://pymongo.readthedocs.io/
- Motor (Async): https://motor.readthedocs.io/
