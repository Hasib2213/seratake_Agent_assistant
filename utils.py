"""
Utility Functions for QMS Platform
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import uuid
import hashlib
from functools import wraps
import time

logger = logging.getLogger(__name__)


def generate_id(prefix: str = "") -> str:
    """Generate unique ID with optional prefix"""
    unique_id = str(uuid.uuid4())
    if prefix:
        return f"{prefix}_{unique_id}"
    return unique_id


def generate_nc_number(org_id: str) -> str:
    """Generate unique non-conformity number"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"NC-{org_id[:3]}-{timestamp}"


def hash_password(password: str) -> str:
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password"""
    return hash_password(password) == hashed


def calculate_risk_score(likelihood: int, impact: int) -> float:
    """Calculate risk score from likelihood and impact"""
    return float(likelihood * impact)


def get_risk_level(score: float) -> str:
    """Get risk level from score"""
    if score <= 5:
        return "Low"
    elif score <= 12:
        return "Medium"
    elif score <= 20:
        return "High"
    else:
        return "Critical"


def get_supplier_performance_score(
    on_time_delivery: float,
    defect_rate: float,
    other_factors: Optional[Dict] = None
) -> float:
    """Calculate supplier performance score (0-100)"""
    # 60% weight on on-time delivery
    # 40% weight on quality (inverse of defect rate)
    
    score = (on_time_delivery * 0.6) + ((100 - defect_rate) * 0.4)
    
    # Apply adjustments based on other factors
    if other_factors:
        if other_factors.get("recent_audit_passed"):
            score += 5
        if other_factors.get("certification"):
            score += 3
        if other_factors.get("complaints"):
            score -= other_factors["complaints"] * 2
    
    return min(100, max(0, score))


def format_date(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object"""
    if isinstance(dt, str):
        return dt
    return dt.strftime(format_str)


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime"""
    return datetime.fromisoformat(date_str)


def get_days_until(target_date: datetime) -> int:
    """Get number of days until target date"""
    delta = target_date - datetime.utcnow()
    return delta.days


def is_overdue(target_date: datetime) -> bool:
    """Check if target date is overdue"""
    return datetime.utcnow() > target_date


def get_quarter(month: int) -> str:
    """Get quarter from month number"""
    if month <= 3:
        return "Q1"
    elif month <= 6:
        return "Q2"
    elif month <= 9:
        return "Q3"
    else:
        return "Q4"


def pagination_params(skip: int = 0, limit: int = 10) -> tuple:
    """Validate pagination parameters"""
    skip = max(0, skip)
    limit = min(100, max(1, limit))  # Max 100 items per page
    return skip, limit


def rate_limit(calls: int = 100, period: int = 60):
    """Rate limiting decorator"""
    def decorator(func):
        calls_made = []
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside the period
            calls_made[:] = [call for call in calls_made if call > now - period]
            
            if len(calls_made) >= calls:
                raise Exception(f"Rate limit exceeded: {calls} calls per {period}s")
            
            calls_made.append(now)
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def log_execution_time(func):
    """Decorator to log function execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f}s: {str(e)}")
            raise
    
    return wrapper


def sanitize_input(value: str, max_length: int = 1000) -> str:
    """Sanitize user input"""
    if not isinstance(value, str):
        return ""
    
    # Remove leading/trailing whitespace
    value = value.strip()
    
    # Truncate if too long
    if len(value) > max_length:
        value = value[:max_length]
    
    # Remove potentially harmful characters
    harmful_chars = ["<", ">", "&", '"', "'", "%"]
    for char in harmful_chars:
        value = value.replace(char, "")
    
    return value


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_iso_standard(standard: str) -> bool:
    """Validate ISO standard format"""
    valid_standards = [
        "ISO 9001",
        "ISO 14001",
        "ISO 45001",
        "ISO 26000",
    ]
    return standard in valid_standards


def convert_to_json(data: Any) -> str:
    """Convert data to JSON string"""
    try:
        return json.dumps(data, default=str)
    except Exception as e:
        logger.error(f"JSON conversion error: {str(e)}")
        return "{}"


def parse_json(data: str) -> Dict:
    """Parse JSON string to dict"""
    try:
        return json.loads(data)
    except Exception as e:
        logger.error(f"JSON parsing error: {str(e)}")
        return {}


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries recursively"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """Flatten nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def build_error_response(
    message: str,
    status_code: int = 500,
    details: Optional[Dict] = None
) -> Dict:
    """Build standardized error response"""
    response = {
        "status": "error",
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    if details:
        response["details"] = details
    
    return response


def build_success_response(
    data: Any,
    message: str = "Success",
    meta: Optional[Dict] = None
) -> Dict:
    """Build standardized success response"""
    response = {
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    if meta:
        response["meta"] = meta
    
    return response


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Chunk a list into smaller lists"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def get_statistical_summary(values: List[float]) -> Dict:
    """Get statistical summary of values"""
    if not values:
        return {}
    
    import statistics
    
    return {
        "min": min(values),
        "max": max(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0,
        "count": len(values),
    }