"""
Apify Web Scraping Tool
Scrapes websites for competitor and market data via Metorial Apify MCP
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from backend.tools.mcp_client import mcp_client
import logging
import asyncio

logger = logging.getLogger(__name__)

class ApifyScraperInput(BaseModel):
    """Input schema for Apify scraper"""
    url: str = Field(..., description="Website URL to scrape (e.g., https://example.com)")
    extract_type: str = Field(
        default="all",
        description="What to extract: 'all' (default), 'text', 'links', or 'metadata'"
    )

class ApifyScraperTool(BaseTool):
    """
    Web scraping tool for extracting company and competitor information
    """
    name: str = "Web Scraper"
    description: str = """
    Scrapes websites to extract comprehensive information about companies, competitors, and markets.

    Use this tool to:
    - Get company information from their website (about, products, team)
    - Scrape competitor websites for features and pricing
    - Extract market data and news articles
    - Gather product descriptions and technical specs

    Returns: Structured data including text content, links, and metadata from the website.
    """
    args_schema: Type[BaseModel] = ApifyScraperInput

    def _run(self, url: str, extract_type: str = "all") -> str:
        """
        Execute web scraping via Metorial Apify MCP

        Args:
            url: Website URL to scrape
            extract_type: Type of data to extract

        Returns:
            Formatted string with scraped content for LLM consumption
        """

        async def scrape():
            try:
                logger.info(f"Scraping {url} (extract_type: {extract_type})")

                # Call MCP via Metorial with direct action command
                # Use imperative language to trigger actual scraping, not explanations
                result = await mcp_client.call_mcp(
                    mcp_name="apify",
                    tool_name="web_scraper",  # For logging only
                    parameters={
                        "url": url,
                        "extract_type": extract_type
                    },
                    natural_message=f"""
                    Call the apify/rag-web-browser actor to scrape {url} right now.

                    Extract all text content, links, and metadata from the page.
                    Return the actual scraped content, not instructions on how to scrape.
                    """
                )

                # Extract text from RunResult
                scraped_content = result.text

                # Format for LLM consumption
                formatted = f"""
=== Web Scraping Results ===
URL: {url}
Extract Type: {extract_type}

Content:
{scraped_content}

=== End of Scraping Results ===
"""

                logger.info(f"Successfully scraped {url}")
                return formatted

            except Exception as e:
                error_msg = f"Error scraping {url}: {str(e)}"
                logger.error(error_msg)
                return f"❌ {error_msg}\n\nPlease try a different URL or check if the website is accessible."

        return asyncio.run(scrape())
