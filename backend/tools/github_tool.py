"""
GitHub Analysis Tool
Analyzes founder GitHub profiles via Metorial GitHub MCP
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from tools.mcp_client import mcp_client
import logging
import asyncio

logger = logging.getLogger(__name__)

class GitHubAnalyzerInput(BaseModel):
    """Input schema for GitHub analyzer"""
    username: str = Field(..., description="GitHub username to analyze (e.g., 'torvalds')")
    include_repos: bool = Field(
        default=True,
        description="Include detailed repository analysis (default: True)"
    )

class GitHubAnalyzerTool(BaseTool):
    """
    GitHub profile and repository analysis tool for founder evaluation
    """
    name: str = "GitHub Analyzer"
    description: str = """
    Analyzes GitHub profiles to evaluate founder technical skills and credibility.

    Use this tool to:
    - Check founder's coding activity and contribution history
    - Analyze repository quality and project diversity
    - Identify technical expertise and programming languages
    - Evaluate code quality and development patterns
    - Look for red flags (inactive account, no substantive projects, plagiarism)
    - Assess open source contributions and community engagement

    Returns: Profile stats, repository analysis, code quality metrics, and technical credibility assessment.
    """
    args_schema: Type[BaseModel] = GitHubAnalyzerInput

    def _run(self, username: str, include_repos: bool = True) -> str:
        """
        Execute GitHub analysis via Metorial GitHub MCP

        Args:
            username: GitHub username to analyze
            include_repos: Whether to include detailed repo analysis

        Returns:
            Formatted string with GitHub profile analysis
        """

        async def analyze():
            try:
                logger.info(f"Analyzing GitHub user '{username}' (include_repos: {include_repos})")

                # Call MCP via Metorial with natural language
                # Let Metorial's LLM choose from available GitHub tools
                result = await mcp_client.call_mcp(
                    mcp_name="github",
                    tool_name="analyze_user",  # For logging only
                    parameters={
                        "username": username,
                        "include_repos": include_repos
                    },
                    natural_message=f"""
                    Analyze the GitHub profile for user "{username}".

                    Please provide:
                    1. **Profile Overview**: Account age, followers, following, public repos count
                    2. **Activity Metrics**: Recent commits, contribution streak, activity level
                    3. **Programming Languages**: Top languages used with percentages
                    4. **Repository Analysis** (if include_repos is True):
                       - Top repositories by stars/forks
                       - Repository quality indicators
                       - Project diversity and complexity
                    5. **Technical Assessment**:
                       - Coding expertise level (beginner, intermediate, advanced, expert)
                       - Areas of specialization
                       - Open source contributions
                    6. **Red Flags**:
                       - Inactive account
                       - No substantive projects
                       - Suspicious patterns
                       - Low code quality

                    Format as a structured technical evaluation suitable for investor due diligence.
                    """
                )

                # Extract text from RunResult
                github_content = result.text

                # Format for LLM consumption
                formatted = f"""
=== GitHub Technical Evaluation ===
Username: @{username}
Repository Analysis: {"Included" if include_repos else "Excluded"}

{github_content}

=== End of GitHub Analysis ===

Technical Credibility Score: Evaluate based on activity, code quality, and project substance.
Red Flags: Watch for inactive accounts, trivial projects, or lack of technical depth.
"""

                logger.info(f"GitHub analysis completed for '{username}'")
                return formatted

            except Exception as e:
                error_msg = f"Error analyzing GitHub user '{username}': {str(e)}"
                logger.error(error_msg)
                return f"❌ {error_msg}\n\nNote: User may not exist or profile may be private."

        return asyncio.run(analyze())
