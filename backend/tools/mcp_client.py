"""
Metorial MCP Client
Handles all communication with Metorial MCP platform

TODO: Implement MCP client for calling external tools
"""

<<<<<<< Updated upstream
import httpx
from typing import Dict, Any
from backend.config import settings
=======
from metorial import Metorial
from openai import AsyncOpenAI
from typing import Dict, Any, Optional
try:
    from backend.config import settings
except ImportError:
    from config import settings
>>>>>>> Stashed changes
import logging

logger = logging.getLogger(__name__)

class MetorialClient:
    """Client for interacting with Metorial MCP platform"""

    def __init__(self):
        self.base_url = settings.metorial_base_url
        self.api_key = settings.metorial_api_key
        self.deployment_ids = {
            "apify": settings.mcp_apify_id,
            "github": settings.mcp_github_id,
            "hackernews": settings.mcp_hackernews_id,
            "gdrive": settings.mcp_gdrive_id,
            "gcalendar": settings.mcp_gcalendar_id,
            "linkedin": settings.mcp_linkedin_id,
        }

<<<<<<< Updated upstream
=======
        # Track which MCPs require OAuth authentication
        # Based on Metorial documentation and actual behavior:
        # - Apify, Google Calendar, Google Drive require OAuth
        # - GitHub may require OAuth depending on Metorial deployment configuration
        #   (Some GitHub MCP deployments require OAuth for API access)
        self.oauth_required = {
            "apify": True,
            "gcalendar": True,
            "gdrive": True,
            "github": True,  # GitHub MCP typically requires OAuth for API access
            "hackernews": False,  # Public API, no auth needed
            "exa": False,  # Uses API key
            "linkedin": False,  # Uses RapidAPI key, no OAuth needed
        }

        # Cache for OAuth sessions (mcp_name -> oauth_session)
        # In production, you might want to persist these (e.g., in database)
        self._oauth_sessions: Dict[str, Any] = {}

    async def create_oauth_session(self, mcp_name: str, auto_wait: bool = True) -> Dict[str, Any]:
        """
        Create an OAuth session for an MCP that requires authentication

        Args:
            mcp_name: Name of MCP (apify, gcalendar, gdrive)
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

            await self.metorial.oauth.wait_for_completion([oauth_session])
            print("✅ OAuth session completed!")

            # Cache the session
            self._oauth_sessions[mcp_name] = oauth_session
            logger.info(f"OAuth session stored for {mcp_name}. Session ID: {oauth_session.id}")
            logger.info(f"OAuth session object: {oauth_session}")
            logger.info(f"OAuth session attributes: {dir(oauth_session)}")
            return {"session": oauth_session, "url": None, "completed": True}
        else:
            # Return URL for manual completion
            return {
                "session": oauth_session,
                "url": oauth_session.url,
                "completed": False
            }

    async def wait_for_oauth_completion(self, oauth_session) -> None:
        """Wait for an OAuth session to complete"""
        await self.metorial.oauth.wait_for_completion([oauth_session])

>>>>>>> Stashed changes
    async def call_mcp(
        self,
        mcp_name: str,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a Metorial MCP tool

        Args:
            mcp_name: Name of MCP (apify, github, etc.)
            tool_name: Specific tool within the MCP
            parameters: Tool parameters

        Returns:
            Tool execution result

        TODO: Implement HTTP call to Metorial API
        """
        # TODO: Implement
        pass

# Global client instance
mcp_client = MetorialClient()
