"""
Exa AI Search Tool
AI-powered search engine for finding relevant content via Metorial Exa MCP
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from backend.tools.mcp_client import mcp_client
import logging
import asyncio

logger = logging.getLogger(__name__)

class ExaSearchInput(BaseModel):
    """Input schema for Exa search"""
    query: str = Field(..., description="Search query for finding relevant content")
    num_results: int = Field(
        default=10,
        description="Number of results to return (default: 10, max: 20)"
    )

class ExaSearchTool(BaseTool):
    """
    AI-powered search tool using Exa search engine
    """
    name: str = "Exa AI Search"
    description: str = """
    AI-powered search engine that finds highly relevant content, articles, and research.

    Use this tool to:
    - Find recent news and articles about companies or markets
    - Discover industry research and reports
    - Search for competitive intelligence
    - Find technical documentation and resources
    - Gather market trends and analysis

    Exa uses AI to understand semantic meaning and return highly relevant results,
    better than traditional keyword-based search for complex queries.

    Returns: Relevant articles, research papers, and web content with summaries.
    """
    args_schema: Type[BaseModel] = ExaSearchInput

    def _run(self, query: str, num_results: int = 10) -> str:
        """
        Execute AI-powered search via Metorial Exa MCP

        Args:
            query: Search query string
            num_results: Number of results to return

        Returns:
            Formatted string with search results and summaries
        """

        async def search():
            try:
                logger.info(f"Searching Exa for '{query}' (num_results: {num_results})")

                # Call MCP via Metorial with natural language
                # Let Metorial's LLM choose from available Exa tools
                result = await mcp_client.call_mcp(
                    mcp_name="exa",
                    tool_name="ai_search",  # For logging only
                    parameters={
                        "query": query,
                        "num_results": num_results
                    },
                    natural_message=f"""
                    Use Exa AI search to find relevant content about "{query}".

                    Please:
                    1. Search for the top {num_results} most relevant results
                    2. Include article titles, URLs, and publication dates
                    3. Provide brief summaries of each result
                    4. Highlight key insights and findings
                    5. Identify authoritative sources vs. general content
                    6. Note any trends or patterns across results

                    Focus on recent, high-quality content relevant for investment research.
                    """
                )

                # Extract text from RunResult
                exa_content = result.text

                # Format for LLM consumption
                formatted = f"""
=== Exa AI Search Results ===
Search Query: "{query}"
Results Found: {num_results}

{exa_content}

=== End of Search Results ===

Note: Exa uses AI-powered semantic search for highly relevant results.
Evaluate source credibility and recency when using this information.
"""

                logger.info(f"Exa search completed for '{query}'")
                return formatted

            except Exception as e:
                error_msg = f"Error searching Exa for '{query}': {str(e)}"
                logger.error(error_msg)
                return f"❌ {error_msg}\n\nNote: Exa MCP server may not be configured or query may be too broad."

        return asyncio.run(search())
