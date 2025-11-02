"""
REST API routes for VC Council
TODO: Implement API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

# Note: Import will work when running from backend/ directory or with proper PYTHONPATH
try:
    from services.crew_orchestrator import VCCouncilOrchestrator
except ImportError:
    from backend.services.crew_orchestrator import VCCouncilOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter()

# Global orchestrator instance
orchestrator = VCCouncilOrchestrator()

# Request/Response models
class AnalysisRequest(BaseModel):
    company_name: str
    website: str
    founder_github: Optional[str] = None
    industry: Optional[str] = None
    product_description: Optional[str] = None
    financial_metrics: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    status: str
    session_id: str
    message: str

@router.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest):
    """
    Start a new investment analysis

    Returns session_id that frontend can use for SSE connection
    """
    try:
        logger.info(f"Starting analysis for {request.company_name}")
        
        # Call orchestrator to start analysis
        session_id = await orchestrator.start_analysis(request.dict())
        
        logger.info(f"Analysis started with session: {session_id}")
        
        return AnalysisResponse(
            status="started",
            session_id=session_id,
            message=f"Analysis started for {request.company_name}"
        )
    except Exception as e:
        logger.error(f"Error starting analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/{session_id}")
async def get_analysis_status(session_id: str):
    """
    Get analysis status and results
    """
    try:
        result = await orchestrator.get_result(session_id)
        
        if result is None:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
