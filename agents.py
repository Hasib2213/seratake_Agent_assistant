"""
LangChain Agents for QMS Platform
Autonomous agents for risk prediction, maintenance scheduling, etc.
"""

import json
import logging
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config import get_settings
settings = get_settings()
logger = logging.getLogger(__name__)


class RiskPredictionAgent:
    """Agent for predicting emerging risks using historical data"""
    
    def __init__(self, db_session=None):
        self.db_session = db_session
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=settings.GEMINI_TEMPERATURE,
            max_output_tokens=settings.GEMINI_MAX_TOKENS,
        )
        self.memory = ChatMessageHistory()
        
    def analyze_historical_incidents(self, org_id: str, days: int = 90) -> Dict:
        """Analyze historical incident data to identify patterns"""
        try:
            # Query incidents from database
            incidents = self._get_incidents(org_id, days)
            
            if not incidents:
                return {"status": "no_data", "message": "No incidents found"}
            
            # Group by category
            categorized = {}
            for incident in incidents:
                cat = incident.get("category", "Unknown")
                if cat not in categorized:
                    categorized[cat] = []
                categorized[cat].append(incident)
            
            return {
                "status": "success",
                "total_incidents": len(incidents),
                "categorized_data": categorized,
                "time_period": f"{days} days",
            }
        except Exception as e:
            logger.error(f"Error analyzing incidents: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def predict_risk_trends(self, analysis_data: Dict) -> Dict:
        """Use AI to predict upcoming risks"""
        try:
            prompt = f"""
            Based on this incident analysis data: {json.dumps(analysis_data)}
            
            Please predict:
            1. What risks are likely to emerge in the next 30 days?
            2. Which categories show increasing trends?
            3. What severity level should we assign?
            4. What preventive actions do you recommend?
            
            Provide structured JSON response.
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            
            return {
                "status": "success",
                "predictions": response.content,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error predicting risks: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _get_incidents(self, org_id: str, days: int):
        """Mock: Fetch incidents from database"""
        # In production, query actual database
        return [
            {
                "date": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                "category": "Safety",
                "severity": "Medium",
            }
            for i in range(5)
        ]
    
    async def execute(self, org_id: str) -> Dict:
        """Execute the risk prediction workflow"""
        try:
            logger.info(f"Starting Risk Prediction Agent for org: {org_id}")
            
            # Step 1: Analyze historical data
            analysis = self.analyze_historical_incidents(org_id)
            if analysis["status"] != "success":
                return analysis
            
            # Step 2: Predict trends
            predictions = self.predict_risk_trends(analysis)
            
            return {
                "status": "success",
                "agent": "RiskPredictionAgent",
                "org_id": org_id,
                "analysis": analysis,
                "predictions": predictions,
                "executed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Risk Prediction Agent failed: {str(e)}")
            return {"status": "error", "message": str(e)}


class PredictiveMaintenanceAgent:
    """Agent for scheduling predictive maintenance based on equipment usage"""
    
    def __init__(self, db_session=None):
        self.db_session = db_session
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.5,  # More deterministic
        )
    
    def get_equipment_data(self, org_id: str) -> Dict:
        """Fetch equipment usage data"""
        try:
            equipment_list = self._fetch_equipment(org_id)
            return {
                "status": "success",
                "equipment_count": len(equipment_list),
                "equipment": equipment_list,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def predict_maintenance_dates(self, equipment_data: Dict) -> Dict:
        """Predict optimal maintenance dates"""
        try:
            prompt = f"""
            Equipment usage data: {json.dumps(equipment_data)}
            
            For each equipment, predict:
            1. Next maintenance date based on usage patterns
            2. Maintenance type needed
            3. Estimated downtime
            4. Priority level
            
            Return as structured JSON.
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            
            return {
                "status": "success",
                "maintenance_schedule": response.content,
                "generated_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _fetch_equipment(self, org_id: str):
        """Mock: Fetch equipment from database"""
        return [
            {
                "id": "eq_001",
                "name": "CNC Machine",
                "usage_hours": 450,
                "last_maintenance": "2024-01-01",
            },
            {
                "id": "eq_002",
                "name": "Pump",
                "usage_hours": 200,
                "last_maintenance": "2024-02-01",
            },
        ]
    
    async def execute(self, org_id: str) -> Dict:
        """Execute predictive maintenance scheduling"""
        try:
            logger.info(f"Starting Predictive Maintenance Agent for org: {org_id}")
            
            equipment_data = self.get_equipment_data(org_id)
            if equipment_data["status"] != "success":
                return equipment_data
            
            schedule = self.predict_maintenance_dates(equipment_data)
            
            return {
                "status": "success",
                "agent": "PredictiveMaintenanceAgent",
                "org_id": org_id,
                "equipment_data": equipment_data,
                "maintenance_schedule": schedule,
                "executed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Predictive Maintenance Agent failed: {str(e)}")
            return {"status": "error", "message": str(e)}


class TrainingGapAnalysisAgent:
    """Agent for analyzing training gaps and assigning tasks"""
    
    def __init__(self, db_session=None):
        self.db_session = db_session
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
        )
    
    def get_skills_matrix(self, org_id: str) -> Dict:
        """Get current skills matrix"""
        return {
            "status": "success",
            "employees": [
                {
                    "id": "emp_001",
                    "name": "John Doe",
                    "role": "Quality Inspector",
                    "skills": ["ISO 9001", "Inspection Techniques"],
                    "missing_skills": ["Risk Analysis", "Audit Procedures"],
                }
            ],
        }
    
    def get_updated_procedures(self, org_id: str) -> Dict:
        """Get recently updated procedures"""
        return {
            "status": "success",
            "updated_documents": [
                {
                    "id": "doc_001",
                    "title": "Quality Inspection Procedure v2.0",
                    "updated_date": datetime.utcnow().isoformat(),
                    "affected_roles": ["Quality Inspector", "Supervisor"],
                }
            ],
        }
    
    def assign_training_tasks(self, skills_data: Dict, documents: Dict) -> Dict:
        """AI assigns training tasks based on gaps"""
        prompt = f"""
        Skills matrix: {json.dumps(skills_data)}
        Updated documents: {json.dumps(documents)}
        
        For each employee with missing skills matching updated documents:
        - Create training task
        - Set priority (High/Medium/Low)
        - Assign deadline
        
        Return as JSON.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {
            "status": "success",
            "training_assignments": response.content,
        }
    
    async def execute(self, org_id: str) -> Dict:
        """Execute training gap analysis"""
        try:
            logger.info(f"Starting Training Gap Analysis Agent for org: {org_id}")
            
            skills = self.get_skills_matrix(org_id)
            documents = self.get_updated_procedures(org_id)
            assignments = self.assign_training_tasks(skills, documents)
            
            return {
                "status": "success",
                "agent": "TrainingGapAnalysisAgent",
                "org_id": org_id,
                "skills_analysis": skills,
                "updated_procedures": documents,
                "training_assignments": assignments,
                "executed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Training Gap Analysis Agent failed: {str(e)}")
            return {"status": "error", "message": str(e)}


class SupplierEvaluationAgent:
    """Agent for analyzing supplier performance and recommending actions"""
    
    def __init__(self, db_session=None):
        self.db_session = db_session
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
        )
    
    def get_supplier_metrics(self, org_id: str) -> Dict:
        """Fetch supplier performance metrics"""
        return {
            "status": "success",
            "suppliers": [
                {
                    "id": "sup_001",
                    "name": "ABC Components",
                    "on_time_delivery": 85,
                    "defect_rate": 2.5,
                    "last_audit": "2024-01-15",
                    "orders_count": 45,
                }
            ],
        }
    
    def analyze_trends(self, supplier_data: Dict) -> Dict:
        """Analyze supplier performance trends"""
        prompt = f"""
        Supplier metrics: {json.dumps(supplier_data)}
        
        For each supplier, analyze:
        1. Performance trend (improving/declining/stable)
        2. Risk factors
        3. Recommended action (continue/audit/renegotiate/replace)
        4. Confidence level
        
        Return structured JSON.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {
            "status": "success",
            "analysis": response.content,
        }
    
    async def execute(self, org_id: str) -> Dict:
        """Execute supplier evaluation"""
        try:
            logger.info(f"Starting Supplier Evaluation Agent for org: {org_id}")
            
            metrics = self.get_supplier_metrics(org_id)
            analysis = self.analyze_trends(metrics)
            
            return {
                "status": "success",
                "agent": "SupplierEvaluationAgent",
                "org_id": org_id,
                "metrics": metrics,
                "analysis": analysis,
                "executed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Supplier Evaluation Agent failed: {str(e)}")
            return {"status": "error", "message": str(e)}


class RootCauseAnalysisAgent:
    """Agent for analyzing non-conformities and suggesting root causes"""
    
    def __init__(self, db_session=None):
        self.db_session = db_session
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
        )
    
    def get_non_conformities(self, org_id: str) -> Dict:
        """Fetch open non-conformities"""
        return {
            "status": "success",
            "non_conformities": [
                {
                    "id": "nc_001",
                    "title": "Incorrect calibration records",
                    "description": "Equipment not calibrated within interval",
                    "date": datetime.utcnow().isoformat(),
                }
            ],
        }
    
    def apply_root_cause_methods(self, nc_data: Dict) -> Dict:
        """Apply 5 Whys and Fishbone methods"""
        prompt = f"""
        Non-conformity: {json.dumps(nc_data)}
        
        Apply both methods:
        1. 5 Whys - drill down to root causes
        2. Fishbone Diagram - categorize by: People, Process, Equipment, Materials, Methods
        
        List top 3-5 probable root causes with confidence levels.
        Return as JSON.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {
            "status": "success",
            "root_cause_analysis": response.content,
        }
    
    async def execute(self, org_id: str) -> Dict:
        """Execute root cause analysis"""
        try:
            logger.info(f"Starting Root Cause Analysis Agent for org: {org_id}")
            
            non_conformities = self.get_non_conformities(org_id)
            analysis = self.apply_root_cause_methods(non_conformities)
            
            return {
                "status": "success",
                "agent": "RootCauseAnalysisAgent",
                "org_id": org_id,
                "non_conformities": non_conformities,
                "root_cause_analysis": analysis,
                "executed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Root Cause Analysis Agent failed: {str(e)}")
            return {"status": "error", "message": str(e)}


# Agent Registry for orchestration
AGENTS = {
    "risk_prediction": RiskPredictionAgent,
    "predictive_maintenance": PredictiveMaintenanceAgent,
    "training_gap_analysis": TrainingGapAnalysisAgent,
    "supplier_evaluation": SupplierEvaluationAgent,
    "root_cause_analysis": RootCauseAnalysisAgent,
}


async def execute_agent(agent_name: str, org_id: str, **kwargs) -> Dict:
    """Execute a specific agent"""
    if agent_name not in AGENTS:
        return {"status": "error", "message": f"Agent '{agent_name}' not found"}
    
    try:
        agent_class = AGENTS[agent_name]
        agent = agent_class()
        result = await agent.execute(org_id, **kwargs)
        return result
    except Exception as e:
        logger.error(f"Error executing agent '{agent_name}': {str(e)}")
        return {"status": "error", "message": str(e)}