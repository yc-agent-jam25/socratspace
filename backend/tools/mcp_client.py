"""
Metorial MCP Client
Handles all communication with Metorial MCP platform using the Metorial SDK
Supports OAuth authentication for services that require it (Google Calendar, Google Drive, etc.)
"""

from metorial import Metorial
from openai import AsyncOpenAI
from typing import Dict, Any, Optional
from config import settings
import logging
import json

logger = logging.getLogger(__name__)

class MetorialClient:
    """Client for interacting with Metorial MCP platform"""

    def __init__(self):
        # Initialize Metorial SDK
        self.metorial = Metorial(api_key=settings.metorial_api_key)

        # Initialize OpenAI client
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

        # Map friendly names to deployment IDs
        self.deployment_ids = {
            "github": settings.mcp_github_id,
            "hackernews": settings.mcp_hackernews_id,
            "exa": settings.mcp_exa_id,
            "gdrive": settings.mcp_gdrive_id,
            "gcalendar": settings.mcp_gcalendar_id,
        }

        # Track which MCPs require OAuth authentication
        # Based on Metorial documentation and actual behavior:
        # - Google Calendar, Google Drive require OAuth
        # - GitHub may require OAuth depending on Metorial deployment configuration
        #   (Some GitHub MCP deployments require OAuth for API access)
        self.oauth_required = {
            "gcalendar": True,
            "gdrive": True,
            "github": True,  # GitHub MCP typically requires OAuth for API access
            "hackernews": False,  # Public API, no auth needed
            "exa": False,  # Uses API key
        }

        # Cache for OAuth sessions (mcp_name -> oauth_session)
        # Also cache pending sessions by session_id for status checking
        # In production, you might want to persist these (e.g., in database)
        self._oauth_sessions: Dict[str, Any] = {}
        self._pending_oauth_sessions: Dict[str, Any] = {}  # session_id -> session object

    async def create_oauth_session(self, mcp_name: str, auto_wait: bool = True) -> Dict[str, Any]:
        """
        Create an OAuth session for an MCP that requires authentication

        Args:
            mcp_name: Name of MCP (gcalendar, gdrive, github)
            auto_wait: If True, wait for OAuth completion automatically. If False, return URL for manual completion.

        Returns:
            Dict with:
                - session: OAuth session object
                - url: URL for user to authenticate (if auto_wait=False)
                - completed: Whether session is completed (if auto_wait=True)

        Raises:
            ValueError: If MCP doesn't require OAuth or deployment ID is missing
        """
        if not self.oauth_required.get(mcp_name, False):
            raise ValueError(f"MCP '{mcp_name}' does not require OAuth authentication")

        deployment_id = self.deployment_ids.get(mcp_name)
        if not deployment_id:
            raise ValueError(f"Deployment ID not configured for MCP: {mcp_name}")

        logger.info(f"Creating OAuth session for {mcp_name}...")

        # Check if we already have a valid session
        if mcp_name in self._oauth_sessions:
            existing_session = self._oauth_sessions[mcp_name]
            # In production, you might want to check if session is still valid
            # For now, we'll reuse it if it exists
            logger.info(f"Reusing existing OAuth session for {mcp_name}")
            return {"session": existing_session, "url": None, "completed": True}

        # Create new OAuth session
        oauth_session = self.metorial.oauth.sessions.create(
            server_deployment_id=deployment_id
        )

        logger.info(f"OAuth session created for {mcp_name}. URL: {oauth_session.url}")

        if auto_wait:
            # Wait for user to complete authentication
            print(f"\n🔗 OAuth Authentication Required for {mcp_name.upper()}")
            print(f"   Please visit this URL to authenticate:")
            print(f"   {oauth_session.url}\n")
            print("⏳ Waiting for OAuth completion...")
            
            # Note: In async context during calendar creation, we can't send SSE easily
            # So we'll use auto_wait=False and handle it via polling in orchestrator
            # For now, just wait (will be handled by calling code)
            await self.metorial.oauth.wait_for_completion([oauth_session])
            print("✅ OAuth session completed!")

            # Cache the session
            self._oauth_sessions[mcp_name] = oauth_session
            # Remove from pending
            if oauth_session.id in self._pending_oauth_sessions:
                del self._pending_oauth_sessions[oauth_session.id]
            logger.info(f"OAuth session stored for {mcp_name}. Session ID: {oauth_session.id}")
            logger.info(f"OAuth session object: {oauth_session}")
            logger.info(f"OAuth session attributes: {dir(oauth_session)}")
            return {"session": oauth_session, "url": None, "completed": True}
        else:
            # Return URL for manual completion
            # Store pending session for status checking
            self._pending_oauth_sessions[oauth_session.id] = oauth_session
            return {
                "session": oauth_session,
                "url": oauth_session.url,
                "completed": False
            }

    async def wait_for_oauth_completion(self, oauth_session) -> None:
        """Wait for an OAuth session to complete"""
        await self.metorial.oauth.wait_for_completion([oauth_session])

    async def call_mcp(
        self,
        mcp_name: str,
        tool_name: str,
        parameters: Dict[str, Any],
        natural_message: str = None,
        oauth_session_id: Optional[str] = None,
        auto_create_oauth: bool = True
    ) -> Dict[str, Any]:
        """
        Call a Metorial MCP tool via the run() method

        Args:
            mcp_name: Name of MCP (github, hackernews, exa, gcalendar, etc.)
            tool_name: Descriptive tool name (for logging only)
            parameters: Tool parameters
            natural_message: Optional natural language instruction (if provided, uses this instead of tool_name)
            oauth_session_id: Optional OAuth session ID (if MCP requires OAuth and session already exists)
            auto_create_oauth: If True, automatically create OAuth session if needed. If False, raise error.

        Returns:
            Tool execution result (RunResult with .text and .steps)

        Raises:
            ValueError: If MCP is unknown or deployment ID is missing
        """
        # Get deployment ID
        deployment_id = self.deployment_ids.get(mcp_name)
        if not deployment_id:
            raise ValueError(f"Unknown MCP: {mcp_name}")

        logger.info(f"Calling {mcp_name}.{tool_name} with params: {parameters}")

        # Handle OAuth if required
        # Based on Metorial docs, all deployments use dict format:
        # OAuth: {"serverDeploymentId": "...", "oauthSessionId": "..."}
        # Non-OAuth: {"serverDeploymentId": "..."}
        
        if self.oauth_required.get(mcp_name, False):
            # OAuth required - build config with session ID
            # Check if we have a session ID provided or cached
            session_id_to_use = oauth_session_id

            if not session_id_to_use:
                if mcp_name in self._oauth_sessions:
                    cached_session = self._oauth_sessions[mcp_name]
                    session_id_to_use = cached_session.id
                    logger.info(f"Using cached OAuth session for {mcp_name}: {session_id_to_use}")
                elif auto_create_oauth:
                    # Create OAuth session automatically
                    logger.info(f"Creating new OAuth session for {mcp_name}...")
                    oauth_result = await self.create_oauth_session(mcp_name, auto_wait=True)
                    session_id_to_use = oauth_result["session"].id
                    logger.info(f"OAuth session created. ID: {session_id_to_use}")
                else:
                    raise ValueError(
                        f"MCP '{mcp_name}' requires OAuth authentication. "
                        f"Please create an OAuth session first using create_oauth_session()"
                    )

            # Build deployment config with OAuth session
            # Verify session ID is a string
            if isinstance(session_id_to_use, str):
                session_id_str = session_id_to_use
            else:
                session_id_str = str(session_id_to_use)
            
            deployment_config = {
                "serverDeploymentId": deployment_id,
                "oauthSessionId": session_id_str
            }
            logger.info(f"Using OAuth session for {mcp_name}: {session_id_str}")
            logger.info(f"Deployment config built: {deployment_config}")
        else:
            # No OAuth - just use deployment ID
            deployment_config = {"serverDeploymentId": deployment_id}

        # Construct message - prefer natural language if provided
        if natural_message:
            # Use natural language and include parameters as context
            message = f"{natural_message}\n\nParameters: {json.dumps(parameters)}"
        else:
            # Fallback to tool name approach
            message = f"Call the {tool_name} tool with these parameters: {json.dumps(parameters)}"

        # Use Metorial's run method with OpenAI
        # All deployments use dict format per Metorial docs
        server_deployments = [deployment_config]
        
        # Debug logging
        logger.info(f"Calling Metorial with deployment config: {deployment_config}")
        logger.info(f"Server deployments: {server_deployments}")

        result = await self.metorial.run(
            message=message,
            server_deployments=server_deployments,
            client=self.openai_client,
            model="gpt-4o",  # Full model with better tool calling support
            max_steps=25  # Allow more steps for complex tool calls
        )

        logger.info(f"MCP call successful: {mcp_name}.{tool_name}")

        # Return RunResult object (has .text and .steps attributes)
        return result

    def clear_oauth_session(self, mcp_name: str):
        """Clear a cached OAuth session"""
        if mcp_name in self._oauth_sessions:
            del self._oauth_sessions[mcp_name]
            logger.info(f"Cleared OAuth session for {mcp_name}")

    def clear_all_oauth_sessions(self):
        """Clear all cached OAuth sessions"""
        self._oauth_sessions.clear()
        logger.info("Cleared all OAuth sessions")

# Global client instance (lazy initialization)
_mcp_client_instance = None

class _MCPClientProxy:
    """Proxy for lazy mcp_client initialization."""
    def __init__(self):
        self._instance = None
    
    def _ensure_instance(self):
        if self._instance is None:
            self._instance = MetorialClient()
        return self._instance
    
    async def create_oauth_session(self, *args, **kwargs):
        return await self._ensure_instance().create_oauth_session(*args, **kwargs)
    
    def call_mcp(self, *args, **kwargs):
        return self._ensure_instance().call_mcp(*args, **kwargs)
    
    def __getattr__(self, name):
        return getattr(self._ensure_instance(), name)

# Global client proxy
mcp_client = _MCPClientProxy()
