"""
Round-based Research Tasks
These initiate each of the 4 discussion rounds with independent, fresh analysis.
"""

from crewai import Task
from typing import List


def create_market_researcher_task(
    agents: dict,
    company_data: dict,
    context: List[Task]
) -> Task:
    """
    Task 1: Market Researcher analyzes market opportunity.

    Context: [] (no previous tasks, fresh start)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see (empty for Task 1)

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")
    website = company_data.get("website", "")
    industry = company_data.get("industry", "")
    product_desc = company_data.get("product_description", "")

    description = f"""
    Research the market opportunity for {company_name}.

    Company details:
    - Website: {website}
    - Industry: {industry}
    - Product: {product_desc}

    Research instructions:
    1. Research the company website to understand their value proposition
    2. Search HackerNews for discussions and sentiment about the product/category
    3. Identify 3-5 direct competitors using available research tools
    4. Estimate TAM using bottom-up or top-down methodology (show calculation)
    5. Determine market growth rate from industry sources
    6. Extract 3-5 key market trends and tailwinds

    IMPORTANT: You will ONLY see this task's context. Focus solely on MARKET analysis.
    The Bull and Bear agents will debate YOUR findings in the next tasks.

    If tools are unavailable, clearly state "Data unavailable" but reason through
    the market analysis using available information and industry knowledge.
    """

    expected_output = """
    Markdown report with the following sections:
    - **TAM Estimate:** $XB with calculation methodology shown
    - **Growth Rate:** X% with source cited
    - **Top Competitors (3-5):** Name + 1-line description each
    - **Market Sentiment:** Positive/Neutral/Negative with HN quotes and links
    - **Key Trends:** 3-5 bullets with supporting data
    """

    # Get the market researcher agent from the agents dict
    market_researcher_agent = agents["market_researcher"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=market_researcher_agent,
        context=context  # Empty list for Task 1
    )


def create_founder_evaluator_task(
    agents: dict,
    company_data: dict,
    context: List[Task]
) -> Task:
    """
    Task 5: Founder Evaluator analyzes founding team.

    Context: [] (no previous tasks, fresh start for Round 2)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see (empty for Task 5)

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")
    founder_github = company_data.get("founder_github", "")
    website = company_data.get("website", "")

    description = f"""
    Evaluate the founding team for {company_name}.

    Founder details:
    - GitHub: {founder_github if founder_github else "Not provided"}
    - Company website: {website}

    Evaluation instructions:
    1. Review GitHub profile (if provided) for technical skills, project quality, contribution history
    2. Analyze team page/LinkedIn for domain expertise and prior relevant experience
    3. Assess execution velocity signals from past projects or companies
    4. Search for red flags: serial entrepreneur failures, ethics issues, team conflicts
    5. Evaluate founder-market fit and passion for the problem

    IMPORTANT: You will ONLY see this task's context. Focus solely on TEAM evaluation.
    This is a FRESH START - you don't see market analysis from Round 1.
    The Bull and Bear agents will debate YOUR findings in the next tasks.

    Team quality is 70% of investment decisions. Be critical but fair.
    If GitHub unavailable, state "GitHub data unavailable" and assess via other signals.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Score:** X/10 (justification required)
    - **Strengths:** Bullet points highlighting technical ability, experience, leadership
    - **Concerns:** Bullet points on gaps, unknowns, or execution risks
    - **Red Flags:** Bullet points on serious concerns (if any)
    - **Evidence:** Links to GitHub, LinkedIn, or other supporting evidence
    """

    # Get the founder evaluator agent from the agents dict
    founder_evaluator_agent = agents["founder_evaluator"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=founder_evaluator_agent,
        context=context  # Empty list for Task 5
    )


def create_product_critic_task(
    agents: dict,
    company_data: dict,
    context: List[Task]
) -> Task:
    """
    Task 9: Product Critic analyzes product moat and defensibility.

    Context: [] (no previous tasks, fresh start for Round 3)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see (empty for Task 9)

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")
    website = company_data.get("website", "")
    product_desc = company_data.get("product_description", "")

    description = f"""
    Analyze the product and competitive defensibility for {company_name}.

    Product details:
    - Website: {website}
    - Description: {product_desc}

    Analysis instructions:
    1. Understand the core product and problem it solves
    2. Identify the moat type (if any): Network effects, Data moat, Scale economies, Brand, Distribution, or None
    3. Assess moat strength on 1-10 scale with justification
    4. Evaluate if a strong competitor could copy in 6 months (Yes/No + detailed reasoning)
    5. List differentiators and assess their sustainability

    IMPORTANT: You will ONLY see this task's context. Focus solely on PRODUCT/MOAT analysis.
    This is a FRESH START - you don't see market or team analysis from previous rounds.
    The Bull and Bear agents will debate YOUR findings in the next tasks.

    Most products lack real moats. Be skeptical. If no moat, explain why.
    If tools unavailable, state "Product data unavailable" but reason through defensibility.
    """

    expected_output = """
    Markdown report with the following sections:
    - **Moat Type(s):** Network / Data / Scale / Brand / Distribution / None
    - **Moat Strength:** X/10 with justification
    - **Copyable in 6 months?:** Yes/No + detailed reasoning
    - **Differentiators:** Bullet points on competitive advantages
    - **Evidence:** Links to product screens, reviews, or market research
    """

    # Get the product critic agent from the agents dict
    product_critic_agent = agents["product_critic"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=product_critic_agent,
        context=context  # Empty list for Task 9
    )


def create_financial_analyst_task(
    agents: dict,
    company_data: dict,
    context: List[Task]
) -> Task:
    """
    Task 13: Financial Analyst evaluates financial health and unit economics.

    Context: [] (no previous tasks, fresh start for Round 4)

    Args:
        agents: Dictionary containing all 8 agent instances
        company_data: User input with company details
        context: List of previous Task objects this task can see (empty for Task 13)

    Returns:
        CrewAI Task object
    """
    company_name = company_data.get("company_name", "the company")
    financial_metrics = company_data.get("financial_metrics", {})

    description = f"""
    Analyze the financial health and unit economics for {company_name}.

    Financial metrics provided:
    {financial_metrics if financial_metrics else "None provided - use conservative industry benchmarks"}

    Analysis instructions:
    1. Extract or assume financial metrics: ARPU, CAC, gross margin, churn rate, monthly burn, cash in bank
    2. Calculate LTV using: ARPU * gross_margin / monthly_churn_rate
    3. Compute LTV:CAC ratio (target: >3:1 for SaaS, >5:1 is exceptional)
    4. Calculate monthly burn and runway in months: cash_bank / monthly_burn
    5. Assess sensitivity to key variables (churn, pricing, CAC)

    IMPORTANT: You will ONLY see this task's context. Focus solely on FINANCIAL analysis.
    This is a FRESH START - you don't see market, team, or product analysis from previous rounds.
    The Bull and Bear agents will debate YOUR findings in the next tasks.

    Use conservative assumptions if data missing. Show all calculations explicitly.
    If key metrics missing, use industry benchmarks and state "Assumed based on industry norms".
    LTV:CAC < 2:1 is a red flag.
    """

    expected_output = """
    Markdown report with the following sections:
    - **LTV:CAC:** X:1 (show calculation: LTV = $Y, CAC = $Z)
    - **Burn & Runway:** $X/month burn, Y months runway
    - **Pricing & Gross Margin Assumptions:** ARPU $X, margin Y%, with sources/assumptions
    - **Financial Health Score:** X/10 based on unit economics and runway
    - **Sensitivity Notes:** Key risks to assumptions (churn, pricing, CAC)
    """

    # Get the financial analyst agent from the agents dict
    financial_analyst_agent = agents["financial_analyst"]

    return Task(
        description=description,
        expected_output=expected_output,
        agent=financial_analyst_agent,
        context=context  # Empty list for Task 13
    )
