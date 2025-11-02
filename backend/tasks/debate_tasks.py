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
    
    CRITICAL: You have access to all research findings from the 5 research agents via context.
    Read and synthesize ALL of their outputs including:
    - Market Research: TAM, growth rate, competitors, sentiment
    - Founder Evaluation: Team quality, execution ability, red flags
    - Product Analysis: Moat strength, defensibility, differentiators
    - Financial Analysis: LTV:CAC, burn rate, runway, financial health
    - Risk Assessment: Top risks, failure scenarios, monitoring plan
    
    Your mission: Champion this investment and find every reason it will succeed.
    
    Instructions:
    1. FIRST, thoroughly read all research outputs from context to understand the full picture
    2. Synthesize all research findings to identify the strongest arguments for investing
    3. Construct investment thesis (3-5 paragraphs) highlighting the core opportunity
    4. Identify top 3 reasons to invest with supporting evidence and numbers from the research
    5. Model upside potential: revenue projection, exit scenarios, ROI estimate
    6. Counter any concerns with data or mitigating factors from the research
    
    IMPORTANT: Reference specific findings from the research agents. Don't repeat generic analysis.
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
    
    CRITICAL: You have access to all research findings from the 5 research agents AND the Bull agent's arguments via context.
    Read and analyze ALL of these outputs including:
    - Market Research: TAM, growth rate, competitors, sentiment
    - Founder Evaluation: Team quality, execution ability, red flags
    - Product Analysis: Moat strength, defensibility, differentiators
    - Financial Analysis: LTV:CAC, burn rate, runway, financial health
    - Risk Assessment: Top risks, failure scenarios, monitoring plan
    - Bull Case: Investment thesis, reasons to invest, upside potential
    
    Your mission: Prevent bad investments by finding every reason this will fail.
    
    Instructions:
    1. FIRST, thoroughly read all research outputs and Bull's arguments from context
    2. Synthesize all research to identify fundamental flaws and weaknesses
    3. Carefully review Bull's arguments and identify weaknesses in their logic and evidence
    4. Construct counter-thesis (2-4 paragraphs) articulating why this investment fails
    5. Identify top 3 reasons NOT to invest with supporting evidence and numbers from research
    6. Model downside/risk scenario with realistic failure modes and potential losses
    7. Provide point-by-point rebuttals to Bull's arguments with evidence
    
    IMPORTANT: Reference specific findings from the research agents and point out flaws in Bull's reasoning.
    Don't just repeat generic concerns - use the actual data to build a rigorous counter-argument.
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
