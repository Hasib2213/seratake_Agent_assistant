# Migration from PostgreSQL to MongoDB Atlas

## Summary of Changes

Your QMS Platform has been successfully configured to use **MongoDB Atlas** instead of PostgreSQL.

## Files Modified

### 1. `requirements.txt`
- ✅ Removed: `sqlalchemy`, `psycopg2-binary`, `alembic`
- ✅ Added: `motor`, `pymongo`, `beanie`

### 2. `config.py`
- ✅ Replaced `DATABASE_URL` with `MONGODB_URI`
- ✅ Added `MONGODB_DB_NAME` configuration

### 3. `database.py`
- ✅ Complete rewrite for MongoDB
- ✅ Uses Motor (async MongoDB driver)
- ✅ Connection pooling configured
- ✅ Automatic index creation
- ✅ Ping test on startup

### 4. `models.py`
- ✅ Converted from SQLAlchemy to Pydantic models
- ✅ All 14 models updated:
  - User, Organization, Document, Risk
  - Policy, Supplier, Equipment, NonConformity
  - Training, Audit, KPI, Notification
  - AIAgentLog, CustomerFeedback
- ✅ Enum classes for status fields
- ✅ Field validation with Pydantic

### 5. `main.py`
- ✅ Updated imports
- ✅ MongoDB connection in lifespan events
- ✅ Removed SQLAlchemy references

## Installation Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `motor==3.3.2` - Async MongoDB driver
- `pymongo==4.6.1` - MongoDB Python driver
- `beanie==1.24.0` - ODM for MongoDB with Pydantic

### Step 2: Configure MongoDB Atlas

1. **Copy environment template:**
   ```bash
   copy .env.example .env
   ```
   (On Linux/Mac: `cp .env.example .env`)

2. **Get MongoDB Atlas connection string:**
   - Follow the detailed guide in `MONGODB_SETUP.md`
   - Or quick steps:
     - Go to https://cloud.mongodb.com/
     - Create free cluster
     - Get connection string
     - Replace `<password>` with your actual password

3. **Update `.env` file:**
   ```env
   MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DB_NAME=qms_db
   GEMINI_API_KEY=your_gemini_api_key
   SECRET_KEY=your-secret-key-here
   ```

### Step 3: Run Application

```bash
python -m uvicorn main:app --reload
```

Or:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 4: Verify Connection

When starting, you should see:
```
INFO - Starting QMS Platform...
INFO - Connecting to MongoDB Atlas...
INFO - Successfully connected to MongoDB Atlas - Database: qms_db
INFO - Creating database indexes...
INFO - Database indexes created successfully
```

## Key Differences: MongoDB vs PostgreSQL

### Data Storage
- **PostgreSQL**: Tables with fixed schema
- **MongoDB**: Collections with flexible documents (JSON-like)

### Models
- **Before (SQLAlchemy)**: ORM with tables and relationships
- **After (Pydantic)**: Document models with validation

### Queries
You'll need to update your query code:

#### Before (SQLAlchemy):
```python
user = db.query(User).filter(User.email == email).first()
```

#### After (MongoDB):
```python
db = get_database()
user = await db.users.find_one({"email": email})
```

### Inserts

#### Before:
```python
db_user = User(email=email, username=username)
db.add(db_user)
db.commit()
```

#### After:
```python
db = get_database()
user_dict = User(email=email, username=username).dict()
result = await db.users.insert_one(user_dict)
```

## Collections Created

The application will automatically create these collections:
- `users`
- `organizations`
- `documents`
- `risks`
- `policies`
- `suppliers`
- `equipment`
- `non_conformities`
- `training`
- `audits`
- `kpis`
- `notifications`
- `ai_agent_logs`
- `customer_feedback`

## Indexes Created Automatically

The `database.py` creates indexes for:
- Users: email (unique), username (unique)
- Organizations: registration_number (unique)
- Documents: title, status, organization_id + doc_type
- Risks: risk_score, title, organization_id + status
- Suppliers: name, organization_id + status

## Data Migration

If you have existing PostgreSQL data:

### Option 1: Manual Migration Script
Create a script to:
1. Export data from PostgreSQL
2. Transform to MongoDB format
3. Import to MongoDB

### Option 2: Fresh Start
Since this is likely development, start fresh with MongoDB.

## Troubleshooting

### Import Errors
If you see `Import "motor.motor_asyncio" could not be resolved`:
```bash
pip install motor pymongo beanie
```

### Connection Timeout
- Check MongoDB Atlas network access
- Ensure IP is whitelisted (0.0.0.0/0 for development)
- Verify username/password

### Authentication Failed
- Check connection string format
- URL-encode special characters in password
- Example: `p@ss` becomes `p%40ss`

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure MongoDB Atlas
3. ✅ Update `.env` file  
4. ✅ Test application startup
5. 🔄 Update API endpoints to use MongoDB queries
6. 🔄 Test all CRUD operations

## Benefits of MongoDB Atlas

✅ **Scalability**: Easy horizontal scaling
✅ **Flexibility**: Schema-less design
✅ **Cloud-native**: Fully managed
✅ **Free tier**: 512MB storage
✅ **Global deployment**: Multi-region
✅ **Automatic backups**: Built-in
✅ **Performance**: Fast JSON operations

## Additional Resources

- 📖 MongoDB Atlas Setup: `MONGODB_SETUP.md`
- 🌐 MongoDB Atlas: https://cloud.mongodb.com/
- 📚 Motor Docs: https://motor.readthedocs.io/
- 📚 Pymongo Docs: https://pymongo.readthedocs.io/

---

**Need Help?** Check `MONGODB_SETUP.md` for detailed MongoDB Atlas setup instructions.
