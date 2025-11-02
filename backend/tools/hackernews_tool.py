"""
HackerNews Sentiment Tool
Searches HackerNews for discussions and sentiment via Metorial HN MCP
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
try:
    from backend.tools.mcp_client import mcp_client
except ImportError:
    from tools.mcp_client import mcp_client
import logging
import asyncio

logger = logging.getLogger(__name__)

class HackerNewsSearchInput(BaseModel):
    """Input schema for HackerNews search"""
    query: str = Field(..., description="Search query (company name, technology, market, etc.)")
    limit: int = Field(
        default=10,
        description="Number of stories to retrieve (default: 10, max: 30)"
    )

class HackerNewsSearchTool(BaseTool):
    """
    HackerNews search and community sentiment analysis tool
    """
    name: str = "HackerNews Search"
    description: str = """
    Searches HackerNews for discussions, sentiment, and community opinions about companies, technologies, and markets.

    Use this tool to:
    - Gauge market sentiment about a company or technology
    - Find technical community opinions and reactions
    - Discover competitive discussions and comparisons
    - Identify potential red flags or controversies
    - Understand developer community interest levels

    Returns: Top stories with points, comments, and sentiment analysis from the HackerNews technical community.
    """
    args_schema: Type[BaseModel] = HackerNewsSearchInput

    def _run(self, query: str, limit: int = 10) -> str:
        """
        Search HackerNews for discussions via Metorial HN MCP

        Args:
            query: Search query string
            limit: Number of stories to retrieve

        Returns:
            Formatted string with HackerNews discussions and sentiment
        """

        async def search():
            try:
                logger.info(f"Searching HackerNews for '{query}' (limit: {limit})")

                # Call MCP via Metorial with natural language
                # Let Metorial's LLM choose from available HN tools (get_top_stories, get_best_stories, etc.)
                result = await mcp_client.call_mcp(
                    mcp_name="hackernews",
                    tool_name="search_stories",  # For logging only
                    parameters={
                        "query": query,
                        "limit": limit
                    },
                    natural_message=f"""
                    Search HackerNews for discussions about "{query}".

                    Please:
                    1. Find the top {limit} most relevant stories about this topic
                    2. Include story titles, points (upvotes), and comment counts
                    3. Provide links to the discussions
                    4. Analyze the overall sentiment (positive, neutral, negative)
                    5. Identify key themes and common discussion points
                    6. Note any controversies or red flags mentioned

                    Format the results in a clear, structured way that helps understand community sentiment.
                    """
                )

                # Extract text from RunResult
                hn_content = result.text

                # Format for LLM consumption
                formatted = f"""
=== HackerNews Community Analysis ===
Search Query: "{query}"
Stories Analyzed: {limit}

{hn_content}

=== End of HackerNews Analysis ===

Note: HackerNews is a technical community. High engagement (points/comments) indicates strong developer interest.
Red flags to watch: Negative sentiment, concerns about business model, technical criticism.
"""

                logger.info(f"HackerNews search completed for '{query}'")
                return formatted

            except Exception as e:
                error_msg = f"Error searching HackerNews for '{query}': {str(e)}"
                logger.error(error_msg)
                return f"❌ {error_msg}\n\nNote: The query might be too specific or no discussions found."

        return asyncio.run(search())
