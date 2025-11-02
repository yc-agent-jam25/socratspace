"""
Round-based Decision Tasks
Risk assessors synthesize debates within each round, and Lead Partner makes final decision.
"""

from crewai import Task
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import List, Literal


# ========== PYDANTIC MODELS ==========

class CalendarEvent(BaseModel):
    """Calendar event model for investment follow-ups."""
    title: str = Field(..., description="Event title")
    start_time: str = Field(..., description="ISO8601 datetime")
    end_time: str = Field(..., description="ISO8601 datetime")
    attendees: List[str] = Field(..., description="List of attendee names")
    description: str = Field(..., description="Event description")


class InvestmentDecision(BaseModel):
    """Structured output for investment decision."""
    decision: Literal["PASS", "MAYBE", "INVEST"] = Field(
        ...,
        description="Investment decision: PASS (fundamental flaws), MAYBE (needs validation), or INVEST (strong opportunity)"
    )
    reasoning: str = Field(
        ...,
        description="3-5 paragraph explanation of decision weighing both sides"
    )
    investment_memo: str = Field(
        ...,
        description="Comprehensive memo summarizing key findings and recommendation"
    )
    calendar_events: List[CalendarEvent] = Field(
        ...,
        description="Calendar events based on decision (PASS=[], MAYBE=1 event, INVEST=2-3 events)"
    )


# ========== RISK ASSESSMENT TASKS ==========

def create_risk_market_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_1, task_2, task_3] - sees all Round 1 discussion
) -> Task:
    """
    Task 4: Risk Assessor evaluates market risks based on Round 1 debate.

    Context: [Tasks 1-3] (market research, bull's market case, bear's market concerns)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Assess risks related to MARKET opportunity based on Round 1 debate for {company_name}.

    You have access to:
    - Market research
    - Bull's case for the market
    - Bear's concerns about the market

    Instructions:
    1. Review all market discussion from context (research, bull arguments, bear concerns)
    2. Identify top 3-5 risks specific to the MARKET opportunity
    3. Rate each risk on two dimensions:
       - Likelihood (1-5): How likely is this risk to materialize?
       - Impact (1-5): How severe would this risk be if it happened?
    4. Propose realistic mitigations for each risk
    5. Create a failure scenario: "How the market opportunity fails"

    IMPORTANT: Focus on MARKET-specific risks only (TAM accuracy, growth assumptions,
    competitive dynamics, market sentiment). You will not see team, product, or financial data.

    Be rigorous and data-driven. Risks with likelihood or impact of 4-5 are serious concerns.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Top 3-5 Market Risks:** Table with columns: Risk | Likelihood (1-5) | Impact (1-5) | Mitigation
    - **Market Failure Scenario:** Narrative of how the market opportunity fails
    - **Risk Assessment Summary:** Overall risk level and key concerns
    """

    # Get the risk assessor agent from the agents dict
    risk_assessor_agent = agents["risk_assessor"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=risk_assessor_agent,
        context=context  # [task_1, task_2, task_3]
    )


def create_risk_team_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_5, task_6, task_7] - sees all Round 2 discussion
) -> Task:
    """
    Task 8: Risk Assessor evaluates execution risks based on Round 2 debate.

    Context: [Tasks 5-7] (founder evaluation, bull's team case, bear's team concerns)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Assess risks related to TEAM execution based on Round 2 debate for {company_name}.

    You have access to:
    - Founder evaluation
    - Bull's case for the team
    - Bear's concerns about the team

    Instructions:
    1. Review all team discussion from context (evaluation, bull arguments, bear concerns)
    2. Identify top 3-5 risks specific to TEAM execution ability
    3. Rate each risk on two dimensions:
       - Likelihood (1-5): How likely is this risk to materialize?
       - Impact (1-5): How severe would this risk be if it happened?
    4. Propose realistic mitigations for each risk
    5. Create a failure scenario: "How the team fails to execute"

    IMPORTANT: Focus on TEAM/EXECUTION-specific risks only (technical gaps, experience deficits,
    red flags, team dynamics). This is a FRESH START - you don't see market analysis.

    Team quality is 70% of investment decisions. Be thorough and critical.
    Risks with likelihood or impact of 4-5 are serious concerns.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Top 3-5 Execution Risks:** Table with columns: Risk | Likelihood (1-5) | Impact (1-5) | Mitigation
    - **Team Failure Scenario:** Narrative of how the team fails to execute
    - **Risk Assessment Summary:** Overall risk level and key concerns
    """

    # Get the risk assessor agent from the agents dict
    risk_assessor_agent = agents["risk_assessor"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=risk_assessor_agent,
        context=context  # [task_5, task_6, task_7]
    )


def create_market_product_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_9, task_10, task_11] - sees all Round 3 discussion
) -> Task:
    """
    Task 12: Market Researcher assesses product-market fit based on Round 3 debate.

    Context: [Tasks 9-11] (product analysis, bull's product case, bear's product concerns)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Assess product-market fit for {company_name} based on Round 3 debate.

    You have access to:
    - Product/moat analysis
    - Bull's case for the product
    - Bear's concerns about the product

    Instructions:
    1. Review all product discussion from context (analysis, bull arguments, bear concerns)
    2. Assess product-market fit on a 1-10 scale with detailed justification
    3. Evaluate if the product actually solves a real pain point customers will pay for
    4. Determine if product differentiation is sufficient to win market share
    5. Analyze whether moat claims are realistic or aspirational

    IMPORTANT: Focus on PRODUCT-MARKET FIT assessment (does this product solve a real problem
    that customers value?). This is a FRESH START - you don't see market or team analysis.

    Be honest and skeptical. Many products lack true product-market fit.
    Consider both bull and bear perspectives carefully.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Product-Market Fit Score:** X/10 with detailed justification
    - **Customer Pain Point Assessment:** Does this solve a real, valuable problem?
    - **Differentiation Validity:** Are the differentiators real or superficial?
    - **Moat Reality Check:** Aspirational vs. realistic defensibility
    - **PMF Summary:** Overall assessment and key concerns/strengths
    """

    # Get the market researcher agent from the agents dict
    # Special case: Market Researcher does PMF assessment in Round 3
    market_researcher_agent = agents["market_researcher"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=market_researcher_agent,
        context=context  # [task_9, task_10, task_11]
    )


def create_risk_financial_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_13, task_14, task_15] - sees all Round 4 discussion
) -> Task:
    """
    Task 16: Risk Assessor evaluates financial risks based on Round 4 debate.

    Context: [Tasks 13-15] (financial analysis, bull's financial case, bear's financial concerns)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Assess risks related to FINANCIAL sustainability based on Round 4 debate for {company_name}.

    You have access to:
    - Financial analysis
    - Bull's case for the financials
    - Bear's concerns about the financials

    Instructions:
    1. Review all financial discussion from context (analysis, bull arguments, bear concerns)
    2. Identify top 3-5 risks specific to FINANCIAL health and unit economics
    3. Rate each risk on two dimensions:
       - Likelihood (1-5): How likely is this risk to materialize?
       - Impact (1-5): How severe would this risk be if it happened?
    4. Propose realistic mitigations for each risk
    5. Create a failure scenario: "How the company runs out of money"

    IMPORTANT: Focus on FINANCIAL-specific risks only (unit economics deterioration, burn rate
    acceleration, runway shortfall, CAC inflation). This is a FRESH START - you don't see
    market, team, or product analysis.

    Be rigorous with numbers. Challenge optimistic assumptions about LTV, CAC, and margins.
    Risks with likelihood or impact of 4-5 are serious concerns.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Top 3-5 Financial Risks:** Table with columns: Risk | Likelihood (1-5) | Impact (1-5) | Mitigation
    - **Financial Failure Scenario:** Narrative of how the company runs out of money
    - **Risk Assessment Summary:** Overall risk level and key concerns
    """

    # Get the risk assessor agent from the agents dict
    risk_assessor_agent = agents["risk_assessor"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=risk_assessor_agent,
        context=context  # [task_13, task_14, task_15]
    )


# ========== FINAL DECISION TASK ==========

def create_lead_partner_decision_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # ALL 16 previous tasks
) -> Task:
    """
    Task 17: Lead Partner makes final PASS/MAYBE/INVEST decision.

    Context: [Tasks 1-16] (ALL previous rounds)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see (all 16 tasks)

    Returns:
        CrewAI Task object with structured output
    """
    company_name = company_data.get("company_name", "this company")

    # Calculate calendar event times
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    two_weeks = today + timedelta(days=14)
    three_months = today + timedelta(days=90)

    description = f"""
    Make the final investment decision for {company_name}.

    You have access to ALL 16 previous tasks via context:

    **Round 1 - Market Discussion:**
    - Task 1: Market research
    - Task 2: Bull's market case
    - Task 3: Bear's market concerns
    - Task 4: Market risk assessment

    **Round 2 - Team Discussion:**
    - Task 5: Founder evaluation
    - Task 6: Bull's team case
    - Task 7: Bear's team concerns
    - Task 8: Execution risk assessment

    **Round 3 - Product Discussion:**
    - Task 9: Product/moat analysis
    - Task 10: Bull's product case
    - Task 11: Bear's product concerns
    - Task 12: Product-market fit assessment

    **Round 4 - Financial Discussion:**
    - Task 13: Financial analysis
    - Task 14: Bull's financial case
    - Task 15: Bear's financial concerns
    - Task 16: Financial risk assessment

    Decision Framework:
    - **PASS:** Fundamental flaws, insurmountable risks, or weak team/product
    - **MAYBE:** Promising but needs validation (traction, key hires, milestones)
    - **INVEST:** Strong opportunity with compelling team, market, product, and economics

    Process:
    1. Read ALL 16 task outputs from context carefully
    2. Synthesize findings across market, team, product, and financial dimensions
    3. Weigh Bull vs Bear arguments on each topic
    4. Identify patterns and contradictions across all rounds
    5. Make decisive decision (PASS/MAYBE/INVEST) with clear reasoning
    6. Generate investment memo and calendar events based on decision

    Calendar Event Rules:
    - **PASS:** calendar_events = [] (empty array)
    - **MAYBE:** 1 event in 90 days (re-evaluation)
      - Title: "Re-evaluate: {company_name} traction review"
      - Start: {three_months.strftime('%Y-%m-%dT14:00:00')}
      - End: {three_months.strftime('%Y-%m-%dT15:00:00')}
      - Attendees: ["Partner: Lead Partner", "IC: Investment Committee"]
    - **INVEST:** 2-3 events within 14 days:
      1. "Due Diligence Kickoff: {company_name}" - {tomorrow.strftime('%Y-%m-%dT14:00:00')} to {tomorrow.strftime('%Y-%m-%dT16:00:00')}
      2. "IC Meeting: {company_name}" - {next_week.strftime('%Y-%m-%dT14:00:00')} to {next_week.strftime('%Y-%m-%dT15:30:00')}
      3. "Term Sheet Discussion: {company_name}" - {two_weeks.strftime('%Y-%m-%dT14:00:00')} to {two_weeks.strftime('%Y-%m-%dT15:00:00')}

    CRITICAL: Your output MUST be valid JSON parseable by Pydantic.
    The InvestmentDecision model expects:
    - decision: "PASS" | "MAYBE" | "INVEST"
    - reasoning: string (3-5 paragraphs weighing all evidence)
    - investment_memo: string (comprehensive summary citing specific findings)
    - calendar_events: array of CalendarEvent objects or empty array

    Your reasoning and memo MUST cite specific findings from the 16 tasks.
    Reference task numbers and specific data points (e.g., "Task 1 showed TAM of $5B growing at 20% YoY").
    """

    expected_output = """
    Valid structured output matching InvestmentDecision Pydantic model:
    - decision: "PASS" | "MAYBE" | "INVEST"
    - reasoning: 3-5 paragraph explanation weighing all evidence across 4 rounds
    - investment_memo: Comprehensive memo summarizing all findings with specific citations
    - calendar_events: Array of events (0 for PASS, 1 for MAYBE, 2-3 for INVEST)
    """

    # Get the lead partner agent
    lead_partner_agent = agents["lead_partner"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=lead_partner_agent,
        context=context,  # ALL 16 previous tasks
        output_pydantic=InvestmentDecision  # Structured output
    )
