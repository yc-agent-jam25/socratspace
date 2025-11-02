"""
Phase 3: Debate Tasks
Bull and Bear agents argue opposite sides with access to all research.
"""

from crewai import Task
from backend.agents.definitions import create_bull_agent, create_bear_agent


def create_bull_case_task(research_tasks: list) -> Task:
    """
    Create Bull agent task to make case FOR investing.

    Args:
        research_tasks: List of 5 research Task objects

    Returns:
        Task object that gets access to all research via context
    """
    description = """
    Build the STRONGEST case FOR investing in this startup.
    
    You have access to all research findings from:
    - Market Research: TAM, growth rate, competitors, sentiment
    - Founder Evaluation: Team quality, execution ability, red flags
    - Product Analysis: Moat strength, defensibility, differentiators
    - Financial Analysis: LTV:CAC, burn rate, runway, financial health
    - Risk Assessment: Top risks, failure scenarios, monitoring plan
    
    Your mission: Champion this investment and find every reason it will succeed.
    
    Instructions:
    1. Synthesize all research findings to identify strengths
    2. Construct investment thesis (3-5 paragraphs) highlighting the core opportunity
    3. Identify top 3 reasons to invest with supporting evidence and numbers
    4. Model upside potential: revenue projection, exit scenarios, ROI estimate
    5. Counter any concerns with data or mitigating factors
    
    You can delegate to research agents if you need more supportive data.
    Be evidence-based but persuasive—use numbers and facts.
    """
    
    expected_output = """
    Markdown report with the following sections:
    - **Investment Thesis:** 3-5 paragraphs making the core case for investment
    - **Top 3 Reasons to Invest:** Bullet points with evidence and numbers
    - **Upside Potential:** Revenue projection, exit scenarios, ROI estimate
    - **Evidence Summary:** Key data points supporting the bull case
    """
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=create_bull_agent(),
        context=research_tasks
    )


def create_bear_case_task(research_tasks: list, bull_task: Task) -> Task:
    """
    Create Bear agent task to make case AGAINST investing.

    Args:
        research_tasks: List of 5 research Task objects
        bull_task: Bull agent's task (Bear can see Bull's arguments)

    Returns:
        Task object that gets access to research + bull case
    """
    description = """
    Build the STRONGEST case AGAINST investing in this startup.
    
    You have access to all research findings from:
    - Market Research: TAM, growth rate, competitors, sentiment
    - Founder Evaluation: Team quality, execution ability, red flags
    - Product Analysis: Moat strength, defensibility, differentiators
    - Financial Analysis: LTV:CAC, burn rate, runway, financial health
    - Risk Assessment: Top risks, failure scenarios, monitoring plan
    
    You also have access to the Bull agent's argument for investing.
    
    Your mission: Prevent bad investments by finding every reason this will fail.
    
    Instructions:
    1. Synthesize all research to identify fundamental flaws and weaknesses
    2. Review Bull's arguments and identify weaknesses in their logic
    3. Construct counter-thesis (2-4 paragraphs) articulating why this fails
    4. Identify top 3 reasons NOT to invest with supporting evidence and numbers
    5. Model downside/risk scenario with realistic failure modes and potential losses
    6. Provide point-by-point rebuttals to Bull's arguments with evidence
    
    You can delegate to research agents if you need more evidence of risks.
    Be rigorous—challenge every assumption and demand evidence.
    """
    
    expected_output = """
    Markdown report with the following sections:
    - **Counter-Thesis:** 2-4 paragraphs articulating why this investment fails
    - **Top 3 Reasons NOT to Invest:** Bullet points with evidence and numbers
    - **Downside/Risk Scenario:** Realistic failure modes and potential losses
    - **Rebuttals to Bull:** Point-by-point challenges to Bull's arguments with evidence
    - **Evidence Summary:** Key data points supporting the bear case
    """
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=create_bear_agent(),
        context=research_tasks + [bull_task]
    )
