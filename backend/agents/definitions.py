"""
CrewAI Agent Definitions for the VC Council investment analysis system.
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
<<<<<<< Updated upstream
from backend.tools._stubs import DummyTool
=======
from backend.tools.apify_tool import ApifyScraperTool
from backend.tools.github_tool import GitHubAnalyzerTool
from backend.tools.hackernews_tool import HackerNewsSearchTool
from backend.tools.exa_tool import ExaSearchTool
from backend.tools.gcalendar_tool import GoogleCalendarTool
from backend.tools.linkedin_tool import LinkedInAnalyzerTool
>>>>>>> Stashed changes

# ========== RESEARCH AGENTS (Phase 1) ==========

def create_market_researcher() -> Agent:
    """
    Create market research specialist agent.

    Configuration:
    - allow_delegation=False: Focus on own research
    - verbose=True: See thinking process
    - max_iter=5: Limit iterations
    - tools: DummyTool (stub until MCP tools ready)
    """
    return Agent(
        role='Market Research Specialist',
        goal='Research and analyze market size, growth, competitive landscape, and sentiment',
        backstory=MARKET_RESEARCHER_PROMPT,
        tools=[DummyTool()],
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_founder_evaluator() -> Agent:
    """
    Create founder evaluation agent.

    Configuration:
    - allow_delegation=False: Focus on own research
    - verbose=True: See thinking process
    - max_iter=5: Limit iterations
    - tools: DummyTool (stub until GitHub/Apify tools ready)
    """
    return Agent(
        role='Founder Evaluator',
        goal='Assess founder background, technical skills, and execution ability',
        backstory=FOUNDER_EVALUATOR_PROMPT,
<<<<<<< Updated upstream
        tools=[DummyTool()],
=======
        tools=[GitHubAnalyzerTool(), LinkedInAnalyzerTool(), ApifyScraperTool()],
>>>>>>> Stashed changes
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_product_critic() -> Agent:
    """
    Create product and moat analysis agent.

    Configuration:
    - allow_delegation=False: Focus on own research
    - verbose=True: See thinking process
    - max_iter=5: Limit iterations
    - tools: DummyTool (stub until Apify tool ready)
    """
    return Agent(
        role='Product Critic',
        goal='Evaluate product defensibility, moat strength, and competitive threats',
        backstory=PRODUCT_CRITIC_PROMPT,
        tools=[DummyTool()],
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_financial_analyst() -> Agent:
    """
    Create financial analyst agent.

    Configuration:
    - allow_delegation=False: Focus on own analysis
    - verbose=True: See thinking process
    - max_iter=5: Limit iterations
    - tools: DummyTool (stub, works primarily with provided data)
    """
    return Agent(
        role='Financial Analyst',
        goal='Calculate LTV:CAC, burn rate, runway, and financial health metrics',
        backstory=FINANCIAL_ANALYST_PROMPT,
        tools=[DummyTool()],
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_risk_assessor() -> Agent:
    """
    Create risk assessment agent.

    Configuration:
    - allow_delegation=False: Focus on own research
    - verbose=True: See thinking process
    - max_iter=5: Limit iterations
    - tools: DummyTool (stub until Apify/HN tools ready)
    """
    return Agent(
        role='Risk Assessor',
        goal='Identify catastrophic failure modes, regulatory risks, and red flags',
        backstory=RISK_ASSESSOR_PROMPT,
        tools=[DummyTool()],
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )

# ========== DEBATE AGENTS (Phase 3) ==========

def create_bull_agent() -> Agent:
    """
    Create Bull advocate agent.

    Configuration:
    - allow_delegation=True: Can ask research agents for more evidence
    - tools=[]: No direct tools, uses research findings
    - max_iter=4: Slightly fewer iterations
    """
    return Agent(
        role='Bull Advocate',
        goal='Build the strongest case FOR investing with compelling evidence',
        backstory=BULL_AGENT_PROMPT,
<<<<<<< Updated upstream
        tools=[],
=======
        tools=[
            ApifyScraperTool(),
            HackerNewsSearchTool(),
            GitHubAnalyzerTool(),
            LinkedInAnalyzerTool(),
            ExaSearchTool()
        ],
>>>>>>> Stashed changes
        verbose=True,
        allow_delegation=True,
        max_iter=4
    )


def create_bear_agent() -> Agent:
    """
    Create Bear advocate agent.

    Configuration:
    - allow_delegation=True: Can ask research agents for more evidence
    - tools=[]: No direct tools, uses research findings
    - max_iter=4: Slightly fewer iterations
    """
    return Agent(
        role='Bear Advocate',
        goal='Build the strongest case AGAINST investing with rigorous evidence',
        backstory=BEAR_AGENT_PROMPT,
<<<<<<< Updated upstream
        tools=[],
=======
        tools=[
            ApifyScraperTool(),
            HackerNewsSearchTool(),
            GitHubAnalyzerTool(),
            LinkedInAnalyzerTool(),
            ExaSearchTool()
        ],
>>>>>>> Stashed changes
        verbose=True,
        allow_delegation=True,
        max_iter=4
    )


# ========== DECISION MAKER (Phase 5) ==========

def create_lead_partner() -> Agent:
    """
    Create Lead Investment Partner agent.

    Configuration:
    - allow_delegation=False: Makes decision independently
    - tools=[]: No tools needed, calendar events in JSON output
    - max_iter=3: Quick decision making
    """
    return Agent(
        role='Lead Investment Partner',
        goal='Make final investment decision (PASS/MAYBE/INVEST) based on all evidence',
        backstory=LEAD_PARTNER_PROMPT,
        tools=[],
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )

# ========== HELPER FUNCTIONS ==========

def create_all_agents() -> dict:
    """
    Create all 8 agents and return as dictionary.

    Returns:
        dict: {agent_id: Agent object} with all 8 agents
    """
    return {
        "market_researcher": create_market_researcher(),
        "founder_evaluator": create_founder_evaluator(),
        "product_critic": create_product_critic(),
        "financial_analyst": create_financial_analyst(),
        "risk_assessor": create_risk_assessor(),
        "bull_agent": create_bull_agent(),
        "bear_agent": create_bear_agent(),
        "lead_partner": create_lead_partner()
    }
