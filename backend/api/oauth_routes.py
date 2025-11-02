"""
OAuth Authentication Routes
Handle OAuth authentication for MCP services (GitHub, Google Calendar, etc.)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from tools.mcp_client import mcp_client

logger = logging.getLogger(__name__)

router = APIRouter()

class OAuthInitiateResponse(BaseModel):
    oauth_session_id: str
    auth_url: str
    status: str = "pending"

class OAuthStatusResponse(BaseModel):
    oauth_session_id: str
    status: str  # "pending", "completed", "failed"
    message: Optional[str] = None

@router.post("/oauth/initiate/{mcp_name}", response_model=OAuthInitiateResponse)
async def initiate_oauth(mcp_name: str):
    """
    Initiate OAuth authentication for an MCP service
    
    Args:
        mcp_name: Name of MCP (github, gcalendar, gdrive)
    
    Returns:
        OAuthInitiateResponse with auth URL and session ID
    
    Raises:
        HTTPException: If MCP doesn't require OAuth or deployment ID is missing
    """
    try:
        logger.info(f"Initiating OAuth for {mcp_name}...")
        
        client_instance = mcp_client._ensure_instance()
        
        # Check if we already have a valid session
        if mcp_name in client_instance._oauth_sessions:
            existing_session = client_instance._oauth_sessions[mcp_name]
            logger.info(f"Reusing existing OAuth session for {mcp_name}: {existing_session.id}")
            return OAuthInitiateResponse(
                oauth_session_id=existing_session.id,
                auth_url=existing_session.url if hasattr(existing_session, 'url') else "",
                status="completed"
            )
        
        # Create OAuth session without waiting (auto_wait=False)
        oauth_result = await mcp_client.create_oauth_session(mcp_name, auto_wait=False)
        
        if not oauth_result.get("url"):
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to get OAuth URL for {mcp_name}"
            )
        
        # Store the session object for later completion checking
        session = oauth_result["session"]
        # Don't cache it yet - wait until it's completed
        
        return OAuthInitiateResponse(
            oauth_session_id=session.id,
            auth_url=oauth_result["url"],
            status="pending"
        )
    
    except ValueError as e:
        logger.error(f"OAuth initiation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"OAuth initiation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to initiate OAuth: {str(e)}")

@router.get("/oauth/status/{oauth_session_id}", response_model=OAuthStatusResponse)
async def check_oauth_status(oauth_session_id: str, mcp_name: str):
    """
    Check OAuth session status
    
    Args:
        oauth_session_id: OAuth session ID from initiate_oauth
        mcp_name: Name of MCP (github, gcalendar, gdrive)
    
    Returns:
        OAuthStatusResponse with current status
    """
    try:
        logger.info(f"Checking OAuth status for {mcp_name} session: {oauth_session_id}")
        
        client_instance = mcp_client._ensure_instance()
        
        # First check cache
        if mcp_name in client_instance._oauth_sessions:
            cached_session = client_instance._oauth_sessions[mcp_name]
            if cached_session.id == oauth_session_id:
                # Session exists in cache, assume completed
                logger.info(f"OAuth session found in cache for {mcp_name}: {oauth_session_id}")
                return OAuthStatusResponse(
                    oauth_session_id=oauth_session_id,
                    status="completed",
                    message="OAuth authentication completed successfully"
                )
        
        # Check if we have a pending session for this ID
        if hasattr(client_instance, '_pending_oauth_sessions'):
            if oauth_session_id in client_instance._pending_oauth_sessions:
                pending_session = client_instance._pending_oauth_sessions[oauth_session_id]
                
                # Try to check if this session is now completed
                # Use wait_for_completion with a very short timeout
                # If session is complete, it returns immediately
                # If still pending, it will timeout
                import asyncio
                try:
                    # Try waiting with a short timeout
                    # If session is already complete, wait_for_completion returns immediately
                    # If still pending, it will timeout
                    logger.debug(f"Checking if OAuth session {oauth_session_id} is completed...")
                    await asyncio.wait_for(
                        client_instance.metorial.oauth.wait_for_completion([pending_session]),
                        timeout=0.5  # 500ms - should be enough if complete, will timeout if pending
                    )
                    # If we get here without timeout, session completed!
                    logger.info(f"✅ OAuth session {oauth_session_id} is now completed!")
                    
                    # Move to completed cache - ensure it's properly stored
                    client_instance._oauth_sessions[mcp_name] = pending_session
                    if oauth_session_id in client_instance._pending_oauth_sessions:
                        del client_instance._pending_oauth_sessions[oauth_session_id]
                    
                    # Log cache status for debugging
                    logger.info(f"OAuth session cached for {mcp_name}. Cached sessions: {list(client_instance._oauth_sessions.keys())}")
                    
                    return OAuthStatusResponse(
                        oauth_session_id=oauth_session_id,
                        status="completed",
                        message="OAuth authentication completed successfully"
                    )
                except asyncio.TimeoutError:
                    # Still pending - timeout means wait_for_completion didn't return quickly
                    # This could mean: 1) session is still pending, or 2) it's complete but took >500ms
                    # Let's assume it's still pending for now
                    logger.debug(f"OAuth session {oauth_session_id} still waiting (timeout)...")
                    pass
                except Exception as wait_error:
                    # Check error message for completion indicators
                    error_str = str(wait_error).lower()
                    logger.debug(f"wait_for_completion error: {wait_error}")
                    
                    # Some errors indicate completion (e.g., "already completed")
                    if any(keyword in error_str for keyword in ['complete', 'finished', 'success', 'already', 'done']):
                        logger.info(f"✅ OAuth session {oauth_session_id} appears completed (from error): {wait_error}")
                        # Move to completed cache
                        client_instance._oauth_sessions[mcp_name] = pending_session
                        if oauth_session_id in client_instance._pending_oauth_sessions:
                            del client_instance._pending_oauth_sessions[oauth_session_id]
                        return OAuthStatusResponse(
                            oauth_session_id=oauth_session_id,
                            status="completed",
                            message="OAuth authentication completed successfully"
                        )
                    # Other error - might be a real error or just means still pending
                    logger.debug(f"Error checking session completion (might be pending): {wait_error}")
                    pass
        
        # Session not found or not completed
        logger.info(f"OAuth session {oauth_session_id} still pending...")
        return OAuthStatusResponse(
            oauth_session_id=oauth_session_id,
            status="pending",
            message="Waiting for authentication..."
        )
    
    except Exception as e:
        logger.error(f"Error checking OAuth status: {e}", exc_info=True)
        return OAuthStatusResponse(
            oauth_session_id=oauth_session_id,
            status="failed",
            message=f"Error checking status: {str(e)}"
        )

@router.post("/oauth/complete/{mcp_name}")
async def complete_oauth(mcp_name: str, oauth_session_id: str):
    """
    Complete OAuth authentication by waiting for user to authenticate
    
    This endpoint can be called to wait for OAuth completion, but the frontend
    should use the status endpoint with polling instead.
    
    Args:
        mcp_name: Name of MCP (github, gcalendar, gdrive)
        oauth_session_id: OAuth session ID from initiate_oauth
    
    Returns:
        dict with completion status
    """
    try:
        logger.info(f"Checking OAuth completion for {mcp_name} session: {oauth_session_id}")
        
        client_instance = mcp_client._ensure_instance()
        
        # Check if session exists in cache
        if mcp_name in client_instance._oauth_sessions:
            session = client_instance._oauth_sessions[mcp_name]
            if session.id == oauth_session_id:
                # Session exists, return completed
                return {
                    "status": "completed",
                    "oauth_session_id": oauth_session_id,
                    "message": "OAuth authentication completed successfully"
                }
        
        # If not in cache, try to wait for it
        # Note: We need the actual session object from initiate, but it's not persisted
        # The frontend polling approach is better
        return {
            "status": "pending",
            "oauth_session_id": oauth_session_id,
            "message": "Waiting for authentication... Please complete authentication in popup."
        }
    
    except Exception as e:
        logger.error(f"Error completing OAuth: {e}", exc_info=True)
        return {
            "status": "failed",
            "oauth_session_id": oauth_session_id,
            "message": f"Error: {str(e)}"
        }

