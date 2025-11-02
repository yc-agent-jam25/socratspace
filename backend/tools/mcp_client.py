"""
Metorial MCP Client
Handles all communication with Metorial MCP platform using the Metorial SDK
"""

from metorial import Metorial
from openai import AsyncOpenAI
from typing import Dict, Any
from backend.config import settings
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
            "apify": settings.mcp_apify_id,
            "github": settings.mcp_github_id,
            "hackernews": settings.mcp_hackernews_id,
            "exa": settings.mcp_exa_id,
            "gdrive": settings.mcp_gdrive_id,
            "gcalendar": settings.mcp_gcalendar_id,
        }

    async def call_mcp(
        self,
        mcp_name: str,
        tool_name: str,
        parameters: Dict[str, Any],
        natural_message: str = None
    ) -> Dict[str, Any]:
        """
        Call a Metorial MCP tool via the run() method

        Args:
            mcp_name: Name of MCP (apify, github, hackernews, exa, etc.)
            tool_name: Descriptive tool name (for logging only)
            parameters: Tool parameters
            natural_message: Optional natural language instruction (if provided, uses this instead of tool_name)

        Returns:
            Tool execution result (RunResult with .text and .steps)
        """
        # Get deployment ID
        deployment_id = self.deployment_ids.get(mcp_name)
        if not deployment_id:
            raise ValueError(f"Unknown MCP: {mcp_name}")

        logger.info(f"Calling {mcp_name}.{tool_name} with params: {parameters}")

        # Construct message - prefer natural language if provided
        if natural_message:
            # Use natural language and include parameters as context
            message = f"{natural_message}\n\nParameters: {json.dumps(parameters)}"
        else:
            # Fallback to tool name approach
            message = f"Call the {tool_name} tool with these parameters: {json.dumps(parameters)}"

        # Use Metorial's run method with OpenAI
        result = await self.metorial.run(
            message=message,
            server_deployments=[deployment_id],
            client=self.openai_client,
            model="gpt-4o"  # Full model with better tool calling support
        )

        logger.info(f"MCP call successful: {mcp_name}.{tool_name}")

        # Return RunResult object (has .text and .steps attributes)
        return result

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
    
    def call_mcp(self, *args, **kwargs):
        return self._ensure_instance().call_mcp(*args, **kwargs)
    
    def __getattr__(self, name):
        return getattr(self._ensure_instance(), name)

# Global client proxy
mcp_client = _MCPClientProxy()
