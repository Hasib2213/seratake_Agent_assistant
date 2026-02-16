import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application Configuration"""
    
    # App Settings
    APP_NAME: str = "QMS Platform - Quality Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # development, staging, production
    
    # API Settings
    API_TITLE: str = "QMS API"
    API_DESCRIPTION: str = "Quality Management System REST API"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB Atlas Configuration
    MONGODB_URI: str = os.getenv(
        "MONGODB_URI",
        "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
    )
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "qms_db")
    
    # Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 1000
    
    # LangChain Configuration
    LANGCHAIN_VERBOSE: bool = False
    LANGCHAIN_DEBUG: bool = False
    
    # Redis Configuration (for Celery & Caching)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["*"]  # Change in production
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list = ["*"]
    ALLOW_HEADERS: list = ["*"]
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    UPLOAD_DIR: str = "./uploads"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Features Configuration
    ENABLE_RISK_PREDICTION: bool = True
    ENABLE_PREDICTIVE_MAINTENANCE: bool = True
    ENABLE_TRAINING_GAP_ANALYSIS: bool = True
    ENABLE_SUPPLIER_EVALUATION: bool = True
    ENABLE_ROOT_CAUSE_ANALYSIS: bool = True
    
    # Notification Settings
    EMAIL_ENABLED: bool = False
    NOTIFICATION_QUEUE: str = "notifications"
    
    # Agent Settings
    AGENTS_CONCURRENCY: int = 5
    AGENTS_TIMEOUT: int = 300  # seconds
    AGENTS_MAX_RETRIES: int = 3
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)"""
    return Settings()


# Predefined roles and permissions
RBAC_CONFIG = {
    "Admin": {
        "permissions": [
            "create_user",
            "edit_user",
            "delete_user",
            "create_policy",
            "edit_policy",
            "approve_documents",
            "manage_compliance",
            "view_reports",
            "manage_agents",
        ]
    },
    "Process_Owner": {
        "permissions": [
            "create_document",
            "edit_document",
            "submit_for_approval",
            "manage_risk",
            "manage_suppliers",
            "view_reports",
        ]
    },
    "Auditor": {
        "permissions": [
            "view_documents",
            "create_audit",
            "view_reports",
            "view_risk",
        ]
    },
    "Viewer": {
        "permissions": [
            "view_documents",
            "view_reports",
        ]
    },
}

# ISO Clauses Mapping
ISO_CLAUSES = {
    "4": "Context of the Organization",
    "5": "Leadership",
    "6": "Planning",
    "7": "Support",
    "8": "Operation",
    "9": "Performance Evaluation",
    "10": "Improvement",
}

# Risk Categories
RISK_CATEGORIES = [
    "Safety",
    "Environmental",
    "Operational",
    "Compliance",
    "Reputational",
    "Financial",
]

# Document Types
DOCUMENT_TYPES = [
    "Policy",
    "Procedure",
    "Work Instruction",
    "Form",
    "Record",
    "Guideline",
]