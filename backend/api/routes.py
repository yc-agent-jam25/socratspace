"""
REST API routes for VC Council
TODO: Implement API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
# TODO: Import when ready
# from backend.services.crew_orchestrator import VCCouncilOrchestrator
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

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

    TODO: Implement to:
    1. Create VCCouncilOrchestrator()
    2. Call orchestrator.start_analysis(request.dict())
    3. Return session_id
    """
    # TODO: Implement
    logger.info(f"TODO: Start analysis for {request.company_name}")
    return AnalysisResponse(
        status="TODO",
        session_id="TODO",
        message=f"TODO: Analysis for {request.company_name}"
    )

@router.get("/analysis/{session_id}")
async def get_analysis_status(session_id: str):
    """
    Get analysis status and results

    TODO: Implement to call orchestrator.get_result(session_id)
    """
    # TODO: Implement
    logger.info(f"TODO: Get analysis {session_id}")
    return {"status": "TODO", "session_id": session_id}
