"""
MongoDB Data Models using Pydantic
"""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid


# Helper function for generating ObjectIds
def generate_uuid() -> str:
    return str(uuid.uuid4())


# ============= User Models =============

class UserRole(str, Enum):
    ADMIN = "Admin"
    PROCESS_OWNER = "Process_Owner"
    AUDITOR = "Auditor"
    VIEWER = "Viewer"


class User(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    email: EmailStr
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    role: str = UserRole.VIEWER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "role": "Viewer"
            }
        }


# ============= Organization Models =============

class Organization(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    name: str
    registration_number: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    iso_standards: List[str] = []  # ["ISO 9001", "ISO 14001", "ISO 45001"]
    scope: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


# ============= Document Models =============

class DocumentStatus(str, Enum):
    DRAFT = "Draft"
    REVIEW = "Review"
    APPROVED = "Approved"
    OBSOLETE = "Obsolete"


class Document(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    title: str
    doc_type: Optional[str] = None  # Policy, Procedure, Work Instruction, etc.
    content: Optional[str] = None
    version: str = "1.0"
    status: str = DocumentStatus.DRAFT
    created_by: str
    approved_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    next_review_date: Optional[datetime] = None
    file_path: Optional[str] = None
    is_current: bool = True
    summary: Optional[str] = None  # AI generated summary
    
    class Config:
        populate_by_name = True


# ============= Risk Models =============

class RiskStatus(str, Enum):
    OPEN = "Open"
    MITIGATED = "Mitigated"
    CLOSED = "Closed"


class Risk(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None  # Safety, Environmental, Operational, etc.
    likelihood: int = Field(ge=1, le=5)  # 1-5
    impact: int = Field(ge=1, le=5)  # 1-5
    risk_score: float = 0.0  # likelihood * impact
    status: str = RiskStatus.OPEN
    owner: Optional[str] = None
    created_by: str
    mitigation_plan: Optional[str] = None
    residual_risk: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    predicted_by_ai: bool = False
    ai_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    class Config:
        populate_by_name = True


# ============= Policy Models =============

class Policy(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    title: str
    iso_clause: Optional[str] = None  # 4, 5, 6, etc.
    content: Optional[str] = None
    approval_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    status: str = "Active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


# ============= Supplier Models =============

class SupplierStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    UNDER_REVIEW = "Under Review"


class Supplier(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    name: str
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None  # Raw Material, Service Provider, etc.
    performance_score: float = 0.0  # 0-100
    on_time_delivery: Optional[float] = None  # %
    defect_rate: Optional[float] = None  # %
    last_audit_date: Optional[datetime] = None
    status: str = SupplierStatus.ACTIVE
    ai_recommendation: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True



# ============= Equipment Models =============

class EquipmentStatus(str, Enum):
    ACTIVE = "Active"
    UNDER_MAINTENANCE = "Under Maintenance"
    RETIRED = "Retired"


class Equipment(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    equipment_name: str
    equipment_code: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    usage_hours: int = 0
    maintenance_frequency: Optional[str] = None  # Monthly, Quarterly, etc.
    calibration_required: bool = False
    calibration_due_date: Optional[datetime] = None
    status: str = EquipmentStatus.ACTIVE
    predicted_maintenance_date: Optional[datetime] = None  # AI predicted
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


# ============= Non-Conformity Models =============

class NCStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CLOSED = "Closed"


class NonConformity(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    nc_number: Optional[str] = None  # Auto-generated
    title: str
    description: Optional[str] = None
    severity: Optional[str] = None  # Minor, Major, Critical
    reported_by: Optional[str] = None
    reported_date: datetime = Field(default_factory=datetime.utcnow)
    root_cause: Optional[str] = None
    root_cause_method: Optional[str] = None  # 5 Whys, Fishbone, etc.
    ai_suggested_causes: Optional[List[str]] = None  # AI predictions
    corrective_action: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[datetime] = None
    status: str = NCStatus.OPEN
    verification_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


# ============= Training Models =============

class TrainingStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    EXPIRED = "Expired"


class Training(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    user_id: str
    training_type: Optional[str] = None  # Induction, Procedure Training, Safety, etc.
    topic: Optional[str] = None
    document_reference: Optional[str] = None  # Document ID
    assigned_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    status: str = TrainingStatus.PENDING
    proficiency_level: Optional[int] = Field(None, ge=1, le=5)  # 1-5
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


# ============= Audit Models =============

class AuditStatus(str, Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class Audit(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    audit_type: Optional[str] = None  # Internal, External, Management Review
    scheduled_date: Optional[datetime] = None
    actual_date: Optional[datetime] = None
    auditor: Optional[str] = None
    scope: Optional[str] = None
    findings: List[dict] = []  # List of findings
    non_conformities_found: int = 0
    status: str = AuditStatus.SCHEDULED
    report_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


# ============= KPI Models =============

class KPIStatus(str, Enum):
    ON_TRACK = "On Track"
    AT_RISK = "At Risk"
    OFF_TRACK = "Off Track"


class KPI(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    name: str
    iso_clause: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    unit: Optional[str] = None  # %, hours, incidents, etc.
    frequency: Optional[str] = None  # Daily, Weekly, Monthly
    owner: Optional[str] = None
    status: Optional[str] = None  # On Track, At Risk, Off Track
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


# ============= Notification Models =============

class NotificationPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Notification(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    user_id: str
    notification_type: Optional[str] = None  # Document Expiry, Risk Alert, Approval Pending
    title: Optional[str] = None
    message: Optional[str] = None
    priority: str = NotificationPriority.MEDIUM
    is_read: bool = False
    action_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True


# ============= AI Agent Log Models =============

class AIAgentLog(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    agent_name: Optional[str] = None  # Risk Predictor, Maintenance Scheduler, etc.
    organization_id: Optional[str] = None
    execution_status: Optional[str] = None  # Success, Failed, Partial
    input_data: Optional[dict] = None
    output_data: Optional[dict] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None  # seconds
    tokens_used: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


# ============= Customer Feedback Models =============

class SentimentType(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class CustomerFeedback(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias="_id")
    organization_id: str
    feedback_text: Optional[str] = None
    sentiment: Optional[str] = None  # Positive, Neutral, Negative
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0)  # -1 to 1
    category: Optional[str] = None  # Product, Service, Support, Delivery
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    ai_analyzed: bool = False
    ai_insights: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
