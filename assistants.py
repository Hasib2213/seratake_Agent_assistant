"""
Gemini AI Assistants for QMS Platform
User-facing AI helpers for document analysis, sentiment analysis, etc.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List, Any
import json
import logging
from datetime import datetime
from config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class DocumentAssistant:
    """AI Assistant for document management and summarization"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.5,
        )
    
    async def summarize_document(self, content: str, max_length: int = 200) -> Dict:
        """Summarize a document using AI"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are a technical document expert. 
                Provide clear, concise summaries focusing on key points and action items."""),
                HumanMessage(content=f"""Summarize this QMS document in {max_length} words:
                
                {content}
                
                Focus on: Purpose, Key Requirements, Compliance Items."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "summary": response.content,
                "word_count": len(response.content.split()),
                "generated_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Document summarization error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def extract_key_points(self, content: str) -> Dict:
        """Extract key points and action items from document"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="Extract key requirements and action items."),
                HumanMessage(content=f"""Analyze this document and extract:
                1. Main Purpose/Scope
                2. Key Requirements (numbered list)
                3. Responsible Parties
                4. Timeline/Deadlines
                5. Success Criteria
                
                Document: {content}
                
                Return as JSON."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "key_points": response.content,
                "analysis_date": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Key points extraction error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def suggest_improvements(self, content: str) -> Dict:
        """Suggest improvements to document clarity and compliance"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a QMS compliance expert."),
                HumanMessage(content=f"""Review this document for improvements:
                
                {content}
                
                Suggest improvements for:
                1. Clarity and Readability
                2. ISO Compliance
                3. Completeness
                4. Consistency
                
                Return as JSON with specific recommendations."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "suggestions": response.content,
                "review_date": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Document improvement suggestion error: {str(e)}")
            return {"status": "error", "message": str(e)}


class SentimentAnalysisAssistant:
    """AI Assistant for analyzing customer feedback and sentiment"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.3,  # Deterministic
        )
    
    async def analyze_feedback(self, feedback_text: str) -> Dict:
        """Analyze customer feedback sentiment"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a sentiment analysis expert."),
                HumanMessage(content=f"""Analyze this customer feedback:
                
                "{feedback_text}"
                
                Provide:
                1. Overall Sentiment (Positive/Neutral/Negative)
                2. Sentiment Score (-1.0 to 1.0)
                3. Key Topics Mentioned
                4. Concerns/Compliments
                5. Recommended Action
                
                Return as JSON."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "analysis": response.content,
                "analyzed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def batch_sentiment_analysis(self, feedback_list: List[str]) -> Dict:
        """Analyze multiple feedback entries"""
        try:
            results = []
            for idx, feedback in enumerate(feedback_list, 1):
                analysis = await self.analyze_feedback(feedback)
                results.append({
                    "feedback_id": idx,
                    "text": feedback,
                    "analysis": analysis,
                })
            
            return {
                "status": "success",
                "total_analyzed": len(feedback_list),
                "results": results,
                "analyzed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Batch sentiment analysis error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def identify_trends(self, feedback_list: List[str]) -> Dict:
        """Identify sentiment trends from feedback"""
        try:
            combined_feedback = "\n".join([f"- {f}" for f in feedback_list])
            
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a data analyst expert."),
                HumanMessage(content=f"""Analyze these customer feedback entries for trends:
                
                {combined_feedback}
                
                Identify:
                1. Common Themes
                2. Problem Areas (if any)
                3. Positive Aspects
                4. Sentiment Distribution
                5. Suggested Improvements
                6. Priority Actions
                
                Return as JSON."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "trends": response.content,
                "sample_size": len(feedback_list),
                "analyzed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Trend identification error: {str(e)}")
            return {"status": "error", "message": str(e)}


class ContextAnalysisAssistant:
    """AI Assistant for strategic context analysis (PESTEL, SWOT)"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
        )
    
    async def pestel_analysis(self, context: str) -> Dict:
        """Perform PESTEL analysis"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a strategic business analyst."),
                HumanMessage(content=f"""Perform a PESTEL analysis based on this context:
                
                {context}
                
                Analyze:
                1. Political Factors
                2. Economic Factors
                3. Social Factors
                4. Technological Factors
                5. Environmental Factors
                6. Legal Factors
                
                For each: List 2-3 key factors and their impact (High/Medium/Low)
                Return as JSON."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "pestel": response.content,
                "analysis_date": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"PESTEL analysis error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def swot_analysis(self, context: str) -> Dict:
        """Perform SWOT analysis"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a strategic planning expert."),
                HumanMessage(content=f"""Conduct a SWOT analysis for:
                
                {context}
                
                Provide:
                1. Strengths (3-5 internal positive factors)
                2. Weaknesses (3-5 internal challenges)
                3. Opportunities (3-5 external positive factors)
                4. Threats (3-5 external challenges)
                
                Return as JSON."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "swot": response.content,
                "analysis_date": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"SWOT analysis error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def tows_matrix(self, swot_data: Dict) -> Dict:
        """Generate TOWS matrix from SWOT analysis"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a strategic strategist."),
                HumanMessage(content=f"""Generate TOWS matrix strategies from this SWOT:
                
                {json.dumps(swot_data)}
                
                Create 4 strategy groups:
                1. Maxi-Maxi (Strengths + Opportunities)
                2. Maxi-Mini (Strengths + Threats)
                3. Mini-Maxi (Weaknesses + Opportunities)
                4. Mini-Mini (Weaknesses + Threats)
                
                For each: Suggest 2-3 actionable strategies
                Return as JSON."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "tows_matrix": response.content,
                "generated_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"TOWS matrix generation error: {str(e)}")
            return {"status": "error", "message": str(e)}


class ComplianceAssistant:
    """AI Assistant for compliance checking and gap analysis"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.5,
        )
    
    async def check_iso_compliance(self, content: str, iso_standard: str = "ISO 9001") -> Dict:
        """Check document compliance with ISO standards"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=f"You are an ISO {iso_standard} compliance expert."),
                HumanMessage(content=f"""Review this document for {iso_standard} compliance:
                
                {content}
                
                Check alignment with:
                1. Clause 4 - Context
                2. Clause 5 - Leadership
                3. Clause 6 - Planning
                4. Clause 7 - Support
                5. Clause 8 - Operation
                6. Clause 9 - Performance Evaluation
                7. Clause 10 - Improvement
                
                For each clause: Compliant/Gap/Not Applicable
                Return as JSON with remediation suggestions for gaps."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "compliance_check": response.content,
                "standard": iso_standard,
                "checked_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"ISO compliance check error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def identify_gaps(self, current_state: str, target_standard: str) -> Dict:
        """Identify compliance gaps"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a compliance gap analyst."),
                HumanMessage(content=f"""Identify gaps between current state and {target_standard}:
                
                Current State: {current_state}
                
                Target: {target_standard}
                
                Provide:
                1. List of Gaps (Priority: High/Medium/Low)
                2. Root Cause for Each Gap
                3. Remediation Plan with Timeline
                4. Resource Requirements
                5. Success Metrics
                
                Return as JSON."""),
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            return {
                "status": "success",
                "gap_analysis": response.content,
                "analyzed_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Gap analysis error: {str(e)}")
            return {"status": "error", "message": str(e)}


# Assistant Registry
ASSISTANTS = {
    "document": DocumentAssistant,
    "sentiment": SentimentAnalysisAssistant,
    "context": ContextAnalysisAssistant,
    "compliance": ComplianceAssistant,
}


async def get_assistant(assistant_type: str) -> Any:
    """Get an assistant instance"""
    if assistant_type not in ASSISTANTS:
        raise ValueError(f"Unknown assistant type: {assistant_type}")
    
    return ASSISTANTS[assistant_type]()


async def call_assistant_method(
    assistant_type: str,
    method_name: str,
    **kwargs
) -> Dict:
    """Call a specific method on an assistant"""
    try:
        assistant = await get_assistant(assistant_type)
        method = getattr(assistant, method_name, None)
        
        if not method:
            return {
                "status": "error",
                "message": f"Method '{method_name}' not found on '{assistant_type}' assistant"
            }
        
        result = await method(**kwargs)
        return result
    except Exception as e:
        logger.error(f"Error calling assistant: {str(e)}")
        return {"status": "error", "message": str(e)}