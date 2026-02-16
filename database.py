"""
Database Configuration and Session Management for MongoDB Atlas
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi
from config import get_settings
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

# MongoDB client instance
mongodb_client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None


async def connect_to_mongodb():
    """Connect to MongoDB Atlas"""
    global mongodb_client, database
    try:
        logger.info("Connecting to MongoDB Atlas...")
        
        # Create MongoDB client with Server API version
        mongodb_client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            server_api=ServerApi('1'),
            maxPoolSize=50,
            minPoolSize=10,
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000
        )
        
        # Get database instance
        database = mongodb_client[settings.MONGODB_DB_NAME]
        
        # Verify connection
        await mongodb_client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB Atlas - Database: {settings.MONGODB_DB_NAME}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")
        raise


async def close_mongodb_connection():
    """Close MongoDB connection"""
    global mongodb_client
    try:
        if mongodb_client:
            logger.info("Closing MongoDB connections...")
            mongodb_client.close()
            logger.info("MongoDB connections closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB: {str(e)}")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if database is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongodb() first.")
    return database


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        logger.info("Creating database indexes...")
        
        # Users collection indexes
        await database.users.create_index("email", unique=True)
        await database.users.create_index("username", unique=True)
        await database.users.create_index([("email", 1)])
        
        # Organizations collection indexes
        await database.organizations.create_index("registration_number", unique=True, sparse=True)
        
        # Documents collection indexes
        await database.documents.create_index([("organization_id", 1), ("doc_type", 1)])
        await database.documents.create_index("status")
        await database.documents.create_index("title")
        
        # Risks collection indexes
        await database.risks.create_index([("organization_id", 1), ("status", 1)])
        await database.risks.create_index("risk_score")
        await database.risks.create_index("title")
        
        # Suppliers collection indexes
        await database.suppliers.create_index("name")
        await database.suppliers.create_index([("organization_id", 1), ("status", 1)])
        
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Error creating indexes: {str(e)}")


# Aliases for backward compatibility
async def init_db():
    """Initialize database - alias for connect_to_mongodb"""
    await connect_to_mongodb()


async def close_db():
    """Close database - alias for close_mongodb_connection"""
    await close_mongodb_connection()


def get_db() -> AsyncIOMotorDatabase:
    """Get database session dependency - alias for get_database"""
    return get_database()