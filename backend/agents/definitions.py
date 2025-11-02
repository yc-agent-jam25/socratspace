"""
CrewAI Agent Definitions
TODO: Create the 8 agent objects with proper configuration
"""

from crewai import Agent
from backend.agents.prompts import (
    MARKET_RESEARCHER_PROMPT,
    FOUNDER_EVALUATOR_PROMPT,
    PRODUCT_CRITIC_PROMPT,
    FINANCIAL_ANALYST_PROMPT,
    RISK_ASSESSOR_PROMPT,
    BULL_AGENT_PROMPT,
    BEAR_AGENT_PROMPT,
    LEAD_PARTNER_PROMPT
)
# TODO: Import tools when ready
# from backend.tools.apify_tool import ApifyScraperTool
# from backend.tools.github_tool import GitHubAnalyzerTool
# from backend.tools.hackernews_tool import HackerNewsSearchTool
# from backend.tools.gcalendar_tool import GoogleCalendarTool

# ========== RESEARCH AGENTS (Phase 1) ==========

def create_market_researcher() -> Agent:
    """
    Create market research specialist agent

    Configuration:
    - allow_delegation=False: Focus on own research
    - verbose=True: See thinking process
    - max_iter=5: Limit iterations
    - tools: ApifyScraperTool(), HackerNewsSearchTool()

    TODO: Implement agent creation
    """
    # TODO: Implement
    return Agent(
        role='Market Research Specialist',
        goal='TODO: Add goal',
        backstory=MARKET_RESEARCHER_PROMPT,
        tools=[],  # TODO: Add tools when ready
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )

def create_founder_evaluator() -> Agent:
    """
    Create founder evaluation agent

    TODO: Implement agent with GitHub and Apify tools
    """
    # TODO: Implement
    pass

def create_product_critic() -> Agent:
    """
    Create product and moat analysis agent

    TODO: Implement agent with Apify tool
    """
    # TODO: Implement
    pass

def create_financial_analyst() -> Agent:
    """
    Create financial analyst agent

    TODO: Implement agent (no tools needed)
    """
    # TODO: Implement
    pass

def create_risk_assessor() -> Agent:
    """
    Create risk assessment agent

    TODO: Implement agent with Apify and HackerNews tools
    """
    # TODO: Implement
    pass

# ========== DEBATE AGENTS (Phase 3) ==========

def create_bull_agent() -> Agent:
    """
    Create Bull advocate agent

    Configuration:
    - allow_delegation=True: Can ask research agents for more evidence
    - tools=[] : No direct tools, uses research findings
    - max_iter=4: Slightly fewer iterations

    TODO: Implement agent creation
    """
    # TODO: Implement
    pass

def create_bear_agent() -> Agent:
    """
    Create Bear advocate agent

    TODO: Implement agent with delegation enabled
    """
    # TODO: Implement
    pass

# ========== DECISION MAKER (Phase 5) ==========

def create_lead_partner() -> Agent:
    """
    Create Lead Investment Partner agent

    Configuration:
    - allow_delegation=False: Makes decision independently
    - tools=[GoogleCalendarTool()]: Can create calendar events
    - max_iter=3: Quick decision making

    TODO: Implement agent creation
    """
    # TODO: Implement
    pass

# ========== HELPER FUNCTIONS ==========

def create_all_agents() -> dict:
    """
    Create all 8 agents and return as dictionary

    Returns:
        dict: {agent_id: Agent object}

    TODO: Implement to return all 8 agents
    """
    # TODO: Implement
    return {
        "market_researcher": create_market_researcher(),
        # TODO: Add other 7 agents
    }
