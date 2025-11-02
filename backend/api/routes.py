"""
REST API routes for VC Council
Handles analysis requests and status polling
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

# Import works from backend/ directory (Railway setup)
from services.crew_orchestrator import VCCouncilOrchestrator

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

@router.options("/analyze")
async def analyze_options():
    """Handle CORS preflight for analyze endpoint"""
    return {}

@router.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest):
    """
    Start a new investment analysis

    Args:
        request: Analysis request with company data

    Returns:
        AnalysisResponse with session_id for tracking
        Frontend should connect to SSE endpoint /api/sse/{session_id} for real-time updates

    Raises:
        HTTPException: If analysis fails to start
    """
    try:
        logger.info(f"Starting analysis for {request.company_name}")

        # Start analysis via orchestrator
        session_id = await orchestrator.start_analysis(request.dict())

        logger.info(f"Analysis started with session: {session_id}")

        return AnalysisResponse(
            status="started",
            session_id=session_id,
            message=f"Analysis started for {request.company_name}. Connect to SSE endpoint /api/sse/{session_id} for real-time updates."
        )

    except Exception as e:
        logger.error(f"Failed to start analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")

@router.get("/analysis/{session_id}")
async def get_analysis_status(session_id: str):
    """
    Get analysis status and results

    Args:
        session_id: Session ID from start_analysis

    Returns:
        dict with status, result, and metadata

    Raises:
        HTTPException: If session not found
    """
    try:
        logger.info(f"Fetching analysis status for {session_id}")

        result = await orchestrator.get_result(session_id)

        if result is None:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Health check endpoint for orchestrator

    Returns:
        dict with health status and active session count
    """
    return {
        "status": "healthy",
        "service": "vc-council-orchestrator",
        "active_sessions": orchestrator.get_session_count()
    }
