"""
Round-based Debate Tasks
Bull and Bear agents argue opposite sides for each topic in isolation.
"""

from crewai import Task
from typing import List


# ========== ROUND 1: MARKET DEBATE ==========

def create_bull_market_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_1] - sees market research
) -> Task:
    """
    Task 2: Bull Agent argues FOR investing based on market analysis.

    Context: [Task 1] (market research)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Build the STRONGEST case FOR investing in {company_name} based on the MARKET opportunity.

    You have access to the Market Research findings via context. Read it carefully.

    Instructions:
    1. Review the market research from context (TAM, growth, competitors, sentiment)
    2. Identify the strongest arguments for why the MARKET supports investment
    3. Provide specific evidence from the research (numbers, trends, competitor gaps)
    4. Explain upside potential if the company captures market share
    5. Counter any obvious market concerns with mitigating factors

    IMPORTANT: Focus your arguments on MARKET opportunity only. You will not see
    team, product, or financial discussions. Be persuasive but evidence-based.

    You can use your tools to find additional supporting evidence if needed.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Market Thesis:** 2-3 paragraphs on why the market opportunity is compelling
    - **Top 3 Market Arguments:** Bullet points with evidence from research
    - **Upside Potential:** Market share scenarios and revenue potential
    - **Evidence Summary:** Key market data points supporting the bull case
    """

    # Get the bull agent from the agents dict
    bull_agent = agents["bull_agent"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=bull_agent,
        context=context  # [task_1]
    )


def create_bear_market_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_1, task_2] - sees market research + bull case
) -> Task:
    """
    Task 3: Bear Agent argues AGAINST investing based on market analysis.

    Context: [Tasks 1-2] (market research, bull's market case)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Build the STRONGEST case AGAINST investing in {company_name} based on the MARKET analysis.

    You have access to:
    - Market research via context
    - Bull's arguments for the market via context

    Instructions:
    1. Review the market research and Bull's arguments from context
    2. Identify fundamental flaws or risks in the MARKET opportunity
    3. Counter Bull's arguments with evidence from the research
    4. Explain downside risks related to market size, competition, or timing
    5. Highlight any red flags in market sentiment or competitive dynamics

    IMPORTANT: Focus on MARKET concerns only. You will not see team, product, or
    financial discussions. Challenge assumptions rigorously.

    You can use your tools to find additional evidence of market risks if needed.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Market Counter-Thesis:** 2-3 paragraphs on why the market opportunity is flawed
    - **Top 3 Market Concerns:** Bullet points with evidence from research
    - **Rebuttals to Bull:** Point-by-point challenges to Bull's market arguments
    - **Evidence Summary:** Key market data points supporting the bear case
    """

    # Get the bear agent from the agents dict
    bear_agent = agents["bear_agent"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=bear_agent,
        context=context  # [task_1, task_2]
    )


# ========== ROUND 2: TEAM DEBATE ==========

def create_bull_team_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_5] - sees founder evaluation
) -> Task:
    """
    Task 6: Bull Agent argues FOR investing based on team analysis.

    Context: [Task 5] (founder evaluation)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Build the STRONGEST case FOR investing in {company_name} based on the TEAM quality.

    You have access to the Founder Evaluation findings via context. Read it carefully.

    Instructions:
    1. Review the founder evaluation from context (score, strengths, concerns, red flags)
    2. Identify the strongest arguments for why the TEAM supports investment
    3. Provide specific evidence from the research (technical ability, experience, execution)
    4. Explain why this team can execute and win in their market
    5. Counter any obvious team concerns with mitigating factors

    IMPORTANT: Focus your arguments on TEAM quality only. You will not see
    market, product, or financial discussions. Be persuasive but evidence-based.

    Team quality is 70% of investment decisions. Build a compelling case.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Team Thesis:** 2-3 paragraphs on why this team will succeed
    - **Top 3 Team Arguments:** Bullet points with evidence from research
    - **Execution Potential:** Why this team can win and execute
    - **Evidence Summary:** Key team data points supporting the bull case
    """

    # Get the bull agent from the agents dict
    bull_agent = agents["bull_agent"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=bull_agent,
        context=context  # [task_5]
    )


def create_bear_team_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_5, task_6] - sees founder eval + bull case
) -> Task:
    """
    Task 7: Bear Agent argues AGAINST investing based on team analysis.

    Context: [Tasks 5-6] (founder evaluation, bull's team case)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Build the STRONGEST case AGAINST investing in {company_name} based on the TEAM analysis.

    You have access to:
    - Founder evaluation via context
    - Bull's arguments for the team via context

    Instructions:
    1. Review the founder evaluation and Bull's arguments from context
    2. Identify fundamental flaws or risks in the TEAM composition/ability
    3. Counter Bull's arguments with evidence from the research
    4. Explain execution risks related to team gaps, experience, or red flags
    5. Highlight any serious concerns about the team's ability to execute

    IMPORTANT: Focus on TEAM concerns only. You will not see market, product, or
    financial discussions. Challenge assumptions rigorously.

    Team quality is 70% of investment decisions. Be thorough about risks.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Team Counter-Thesis:** 2-3 paragraphs on why this team will struggle
    - **Top 3 Team Concerns:** Bullet points with evidence from research
    - **Rebuttals to Bull:** Point-by-point challenges to Bull's team arguments
    - **Evidence Summary:** Key team data points supporting the bear case
    """

    # Get the bear agent from the agents dict
    bear_agent = agents["bear_agent"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=bear_agent,
        context=context  # [task_5, task_6]
    )


# ========== ROUND 3: PRODUCT DEBATE ==========

def create_bull_product_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_9] - sees product analysis
) -> Task:
    """
    Task 10: Bull Agent argues FOR investing based on product analysis.

    Context: [Task 9] (product/moat analysis)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Build the STRONGEST case FOR investing in {company_name} based on the PRODUCT/MOAT.

    You have access to the Product Analysis findings via context. Read it carefully.

    Instructions:
    1. Review the product analysis from context (moat type, strength, defensibility)
    2. Identify the strongest arguments for why the PRODUCT supports investment
    3. Provide specific evidence from the research (moat strength, differentiators)
    4. Explain why this product is defensible and can sustain competitive advantage
    5. Counter any obvious product concerns with mitigating factors

    IMPORTANT: Focus your arguments on PRODUCT/MOAT only. You will not see
    market, team, or financial discussions. Be persuasive but evidence-based.

    Even weak moats can be strengthened. Build the most optimistic case.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Product Thesis:** 2-3 paragraphs on why this product is defensible
    - **Top 3 Product Arguments:** Bullet points with evidence from research
    - **Competitive Advantage:** Why competitors can't easily replicate
    - **Evidence Summary:** Key product data points supporting the bull case
    """

    # Get the bull agent from the agents dict
    bull_agent = agents["bull_agent"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=bull_agent,
        context=context  # [task_9]
    )


def create_bear_product_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_9, task_10] - sees product analysis + bull case
) -> Task:
    """
    Task 11: Bear Agent argues AGAINST investing based on product analysis.

    Context: [Tasks 9-10] (product analysis, bull's product case)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Build the STRONGEST case AGAINST investing in {company_name} based on the PRODUCT analysis.

    You have access to:
    - Product analysis via context
    - Bull's arguments for the product via context

    Instructions:
    1. Review the product analysis and Bull's arguments from context
    2. Identify fundamental flaws or risks in the PRODUCT defensibility
    3. Counter Bull's arguments with evidence from the research
    4. Explain competitive risks related to copyability, lack of moat, or weak differentiation
    5. Highlight any red flags about product sustainability

    IMPORTANT: Focus on PRODUCT concerns only. You will not see market, team, or
    financial discussions. Challenge assumptions rigorously.

    Most products lack real moats. Be skeptical and evidence-based.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Product Counter-Thesis:** 2-3 paragraphs on why this product is not defensible
    - **Top 3 Product Concerns:** Bullet points with evidence from research
    - **Rebuttals to Bull:** Point-by-point challenges to Bull's product arguments
    - **Evidence Summary:** Key product data points supporting the bear case
    """

    # Get the bear agent from the agents dict
    bear_agent = agents["bear_agent"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=bear_agent,
        context=context  # [task_9, task_10]
    )


# ========== ROUND 4: FINANCIAL DEBATE ==========

def create_bull_financial_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_13] - sees financial analysis
) -> Task:
    """
    Task 14: Bull Agent argues FOR investing based on financial analysis.

    Context: [Task 13] (financial analysis)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Build the STRONGEST case FOR investing in {company_name} based on the FINANCIALS.

    You have access to the Financial Analysis findings via context. Read it carefully.

    Instructions:
    1. Review the financial analysis from context (LTV:CAC, burn, runway, health score)
    2. Identify the strongest arguments for why the FINANCIALS support investment
    3. Provide specific evidence from the research (unit economics, margins, efficiency)
    4. Explain upside potential if the company improves key financial metrics
    5. Counter any obvious financial concerns with mitigating factors

    IMPORTANT: Focus your arguments on FINANCIALS only. You will not see
    market, team, or product discussions. Be persuasive but evidence-based.

    Even mediocre unit economics can improve. Build the optimistic case.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Financial Thesis:** 2-3 paragraphs on why the financials are solid/improving
    - **Top 3 Financial Arguments:** Bullet points with evidence from research
    - **Upside Scenarios:** How financials improve with scale or optimization
    - **Evidence Summary:** Key financial data points supporting the bull case
    """

    # Get the bull agent from the agents dict
    bull_agent = agents["bull_agent"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=bull_agent,
        context=context  # [task_13]
    )


def create_bear_financial_task(
    agents: dict,
    company_data: dict,
    context: List[Task]  # [task_13, task_14] - sees financial analysis + bull case
) -> Task:
    """
    Task 15: Bear Agent argues AGAINST investing based on financial analysis.

    Context: [Tasks 13-14] (financial analysis, bull's financial case)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")

    description = f"""
    Build the STRONGEST case AGAINST investing in {company_name} based on the FINANCIAL analysis.

    You have access to:
    - Financial analysis via context
    - Bull's arguments for the financials via context

    Instructions:
    1. Review the financial analysis and Bull's arguments from context
    2. Identify fundamental flaws or risks in the FINANCIAL metrics
    3. Counter Bull's arguments with evidence from the research
    4. Explain financial risks related to burn rate, unit economics, or runway
    5. Highlight any red flags about financial sustainability

    IMPORTANT: Focus on FINANCIAL concerns only. You will not see market, team, or
    product discussions. Challenge assumptions rigorously.

    Bad unit economics rarely improve. Be skeptical and data-driven.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Financial Counter-Thesis:** 2-3 paragraphs on why the financials are concerning
    - **Top 3 Financial Concerns:** Bullet points with evidence from research
    - **Rebuttals to Bull:** Point-by-point challenges to Bull's financial arguments
    - **Evidence Summary:** Key financial data points supporting the bear case
    """

    # Get the bear agent from the agents dict
    bear_agent = agents["bear_agent"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=bear_agent,
        context=context  # [task_13, task_14]
    )
