"""
FastAPI Backend for Socrat Space
Main application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from config import settings
from api.routes import router
from api.sse import sse_manager
from api.sse_test import create_test_sse_endpoint, generate_mock_events
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Socrat Space API",
    description="AI Investment Intelligence - 8-Agent Investment Committee",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST routes
app.include_router(router, prefix="/api")

# CORS preflight for SSE
@app.options("/api/sse/{session_id}")
async def sse_options(session_id: str, request: Request):
    """Handle CORS preflight for SSE endpoint"""
    from fastapi.responses import Response
    origin = request.headers.get("origin", "*")
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": origin if origin else "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Cache-Control",
        }
    )

# SSE endpoint for real-time updates (production)
@app.get("/api/sse/{session_id}")
async def sse_endpoint(session_id: str, request: Request):
    """
    Server-Side Events endpoint for real-time debate updates
    
    Args:
        session_id: Session ID to stream events for
        request: FastAPI request object (used to detect disconnection)
    
    Returns:
        StreamingResponse with SSE format
    
    Note: When backend orchestrator is ready, this will use sse_manager.
    Currently uses test endpoint for mock events.
    """
    logger.info(f"SSE connection requested for session: {session_id}")

    # Get origin from request
    origin = request.headers.get("origin", "*")

    # Use real SSE manager connected to orchestrator
    event_generator = sse_manager.stream_events(session_id, request)

    # Mock implementation (disabled):
    # event_generator = generate_mock_events(session_id, request)
    
    response = StreamingResponse(
        event_generator,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": origin if origin else "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Cache-Control, Last-Event-ID",
        }
    )
    
    return response


# Test SSE endpoint (explicit test route - can be removed later)
@app.get("/api/sse/test/{session_id}")
async def sse_test_endpoint(session_id: str, request: Request):
    """
    Test SSE endpoint that generates mock events
    Use this for testing frontend SSE integration without full backend
    """
    logger.info(f"Test SSE connection requested for session: {session_id}")
    return create_test_sse_endpoint(session_id, request)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "socrat-space"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True
    )
