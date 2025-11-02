"""
Stub tools used before MCP tools are integrated.
These are temporary placeholder tools that allow the agent system to run
without external tool dependencies.
"""

from crewai.tools import BaseTool


class DummyTool(BaseTool):
    """No-op tool used before MCP tools are integrated."""
    
    name: str = "Dummy"
    description: str = "No-op tool used before MCP tools are integrated."
    
    def _run(self, *args, **kwargs) -> str:
        """Return stub response for all tool calls."""
        return "stub"

