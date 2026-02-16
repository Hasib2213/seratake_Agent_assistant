"""
QMS Platform - Main FastAPI Application
Production-grade Quality Management System with AI
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

from config import get_settings, RBAC_CONFIG, ISO_CLAUSES
from agents import execute_agent
from assistants import call_assistant_method
from database import connect_to_mongodb, close_mongodb_connection, get_database
import utils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting QMS Platform...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"API Version: {settings.API_V1_STR}")
    
    # Connect to MongoDB
    await connect_to_mongodb()
    
    yield
    
    # Shutdown
    logger.info("Shutting down QMS Platform...")
    await close_mongodb_connection()


# Initialize FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)


# ============ HEALTH & STATUS ENDPOINTS ============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "api_docs": "/docs",
        "api_version": settings.API_V1_STR,
    }


# ============ AGENT ENDPOINTS ============

@app.post(f"{settings.API_V1_STR}/agents/risk-prediction")
async def run_risk_prediction(org_id: str):
    """
    Execute Risk Prediction Agent
    Analyzes historical data and predicts emerging risks
    """
    try:
        logger.info(f"Risk Prediction Agent started for org: {org_id}")
        result = await execute_agent("risk_prediction", org_id)
        
        return {
            "status": "success",
            "data": result,
            "executed_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Risk Prediction Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/agents/predictive-maintenance")
async def run_predictive_maintenance(org_id: str):
    """
    Execute Predictive Maintenance Agent
    Schedules maintenance based on equipment usage patterns
    """
    try:
        logger.info(f"Predictive Maintenance Agent started for org: {org_id}")
        result = await execute_agent("predictive_maintenance", org_id)
        
        return {
            "status": "success",
            "data": result,
            "executed_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Predictive Maintenance Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/agents/training-gaps")
async def run_training_gap_analysis(org_id: str):
    """
    Execute Training Gap Analysis Agent
    Identifies missing skills and assigns training tasks
    """
    try:
        logger.info(f"Training Gap Analysis Agent started for org: {org_id}")
        result = await execute_agent("training_gap_analysis", org_id)
        
        return {
            "status": "success",
            "data": result,
            "executed_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Training Gap Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/agents/supplier-evaluation")
async def run_supplier_evaluation(org_id: str):
    """
    Execute Supplier Evaluation Agent
    Analyzes supplier performance and recommends actions
    """
    try:
        logger.info(f"Supplier Evaluation Agent started for org: {org_id}")
        result = await execute_agent("supplier_evaluation", org_id)
        
        return {
            "status": "success",
            "data": result,
            "executed_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Supplier Evaluation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/agents/root-cause-analysis")
async def run_root_cause_analysis(org_id: str):
    """
    Execute Root Cause Analysis Agent
    Analyzes non-conformities using 5 Whys and Fishbone methods
    """
    try:
        logger.info(f"Root Cause Analysis Agent started for org: {org_id}")
        result = await execute_agent("root_cause_analysis", org_id)
        
        return {
            "status": "success",
            "data": result,
            "executed_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Root Cause Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/agents/run-all")
async def run_all_agents(org_id: str):
    """
    Execute all agents for an organization
    Useful for periodic batch processing
    """
    try:
        logger.info(f"Running all agents for org: {org_id}")
        
        agents_to_run = [
            "risk_prediction",
            "predictive_maintenance",
            "training_gap_analysis",
            "supplier_evaluation",
            "root_cause_analysis",
        ]
        
        results = {}
        for agent_name in agents_to_run:
            try:
                result = await execute_agent(agent_name, org_id)
                results[agent_name] = result
            except Exception as e:
                logger.error(f"Error running {agent_name}: {str(e)}")
                results[agent_name] = {"status": "error", "message": str(e)}
        
        return {
            "status": "completed",
            "org_id": org_id,
            "agents_executed": len(agents_to_run),
            "results": results,
            "executed_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Batch agent execution error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ DOCUMENT ASSISTANT ENDPOINTS ============

@app.post(f"{settings.API_V1_STR}/assistant/document/summarize")
async def summarize_document(content: str, max_length: int = 200):
    """
    Summarize a QMS document using AI
    """
    try:
        result = await call_assistant_method(
            "document",
            "summarize_document",
            content=content,
            max_length=max_length
        )
        return result
    except Exception as e:
        logger.error(f"Document summarization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/assistant/document/key-points")
async def extract_document_key_points(content: str):
    """
    Extract key points and action items from document
    """
    try:
        result = await call_assistant_method(
            "document",
            "extract_key_points",
            content=content
        )
        return result
    except Exception as e:
        logger.error(f"Key points extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/assistant/document/improve")
async def suggest_document_improvements(content: str):
    """
    Get AI suggestions for document improvements
    """
    try:
        result = await call_assistant_method(
            "document",
            "suggest_improvements",
            content=content
        )
        return result
    except Exception as e:
        logger.error(f"Document improvement suggestion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ SENTIMENT ANALYSIS ENDPOINTS ============

@app.post(f"{settings.API_V1_STR}/assistant/sentiment/analyze")
async def analyze_feedback_sentiment(feedback: str):
    """
    Analyze customer feedback sentiment
    """
    try:
        result = await call_assistant_method(
            "sentiment",
            "analyze_feedback",
            feedback_text=feedback
        )
        return result
    except Exception as e:
        logger.error(f"Sentiment analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/assistant/sentiment/batch")
async def batch_sentiment_analysis(feedback_list: List[str]):
    """
    Analyze multiple feedback entries
    """
    try:
        result = await call_assistant_method(
            "sentiment",
            "batch_sentiment_analysis",
            feedback_list=feedback_list
        )
        return result
    except Exception as e:
        logger.error(f"Batch sentiment analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/assistant/sentiment/trends")
async def identify_sentiment_trends(feedback_list: List[str]):
    """
    Identify sentiment trends from feedback
    """
    try:
        result = await call_assistant_method(
            "sentiment",
            "identify_trends",
            feedback_list=feedback_list
        )
        return result
    except Exception as e:
        logger.error(f"Trend identification error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ CONTEXT ANALYSIS ENDPOINTS ============

@app.post(f"{settings.API_V1_STR}/assistant/context/pestel")
async def perform_pestel_analysis(context: str):
    """
    Perform PESTEL analysis for strategic planning
    """
    try:
        result = await call_assistant_method(
            "context",
            "pestel_analysis",
            context=context
        )
        return result
    except Exception as e:
        logger.error(f"PESTEL analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/assistant/context/swot")
async def perform_swot_analysis(context: str):
    """
    Perform SWOT analysis
    """
    try:
        result = await call_assistant_method(
            "context",
            "swot_analysis",
            context=context
        )
        return result
    except Exception as e:
        logger.error(f"SWOT analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/assistant/context/tows")
async def generate_tows_matrix(swot_data: Dict):
    """
    Generate TOWS matrix from SWOT analysis
    """
    try:
        result = await call_assistant_method(
            "context",
            "tows_matrix",
            swot_data=swot_data
        )
        return result
    except Exception as e:
        logger.error(f"TOWS matrix generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ COMPLIANCE ENDPOINTS ============

@app.post(f"{settings.API_V1_STR}/assistant/compliance/check")
async def check_iso_compliance(content: str, standard: str = "ISO 9001"):
    """
    Check document compliance with ISO standards
    """
    try:
        result = await call_assistant_method(
            "compliance",
            "check_iso_compliance",
            content=content,
            iso_standard=standard
        )
        return result
    except Exception as e:
        logger.error(f"Compliance check error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(f"{settings.API_V1_STR}/assistant/compliance/gaps")
async def identify_compliance_gaps(current_state: str, target_standard: str):
    """
    Identify compliance gaps
    """
    try:
        result = await call_assistant_method(
            "compliance",
            "identify_gaps",
            current_state=current_state,
            target_standard=target_standard
        )
        return result
    except Exception as e:
        logger.error(f"Gap analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ CONFIGURATION ENDPOINTS ============

@app.get(f"{settings.API_V1_STR}/config/iso-clauses")
async def get_iso_clauses():
    """Get available ISO clauses"""
    return {
        "status": "success",
        "iso_clauses": ISO_CLAUSES,
    }


@app.get(f"{settings.API_V1_STR}/config/rbac")
async def get_rbac_config():
    """Get RBAC configuration"""
    return {
        "status": "success",
        "rbac": RBAC_CONFIG,
    }


@app.get(f"{settings.API_V1_STR}/config/features")
async def get_features_config():
    """Get enabled features"""
    return {
        "status": "success",
        "features": {
            "risk_prediction": settings.ENABLE_RISK_PREDICTION,
            "predictive_maintenance": settings.ENABLE_PREDICTIVE_MAINTENANCE,
            "training_gap_analysis": settings.ENABLE_TRAINING_GAP_ANALYSIS,
            "supplier_evaluation": settings.ENABLE_SUPPLIER_EVALUATION,
            "root_cause_analysis": settings.ENABLE_ROOT_CAUSE_ANALYSIS,
        },
    }


# ============ ERROR HANDLERS ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )