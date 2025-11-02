"""
Phase 1: Research Tasks
These run in parallel for maximum speed and provide inputs to debate agents.
"""

from crewai import Task
from backend.agents.definitions import (
    create_market_researcher,
    create_founder_evaluator,
    create_product_critic,
    create_financial_analyst,
    create_risk_assessor
)

def create_market_research_task(company_data: dict) -> Task:
    """
    Create market research task.

    Args:
        company_data: User input with company_name, website, industry, etc.

    Returns:
        Task object for market researcher agent
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
    1. Scrape the company website to understand their value proposition
    2. Search HackerNews for discussions and sentiment about the product/category
    3. Identify 3-5 direct competitors and their positioning
    4. Estimate TAM using bottom-up or top-down methodology (show calculation)
    5. Determine market growth rate from industry sources
    6. Extract 3-5 key market trends and tailwinds
    
    If tools are unavailable, clearly state "Data unavailable" but reason through the market analysis
    using available information and industry knowledge.
    """
    
    expected_output = """
    Markdown report with the following sections:
    - **TAM Estimate:** $XB with calculation methodology shown
    - **Growth Rate:** X% with source cited
    - **Top Competitors (3-5):** Name + 1-line description each
    - **Market Sentiment:** Positive/Neutral/Negative with HN quotes and links
    - **Key Trends:** 3-5 bullets with supporting data
    """
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=create_market_researcher()
    )


def create_founder_evaluation_task(company_data: dict) -> Task:
    """
    Create founder evaluation task.

    Args:
        company_data: User input with founder details, GitHub, etc.

    Returns:
        Task object for founder evaluator agent
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
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=create_founder_evaluator()
    )


def create_product_analysis_task(company_data: dict) -> Task:
    """
    Create product and moat analysis task.

    Args:
        company_data: User input with product details.

    Returns:
        Task object for product critic agent
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
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=create_product_critic()
    )


def create_financial_analysis_task(company_data: dict) -> Task:
    """
    Create financial analysis task.

    Args:
        company_data: User input with financial metrics.

    Returns:
        Task object for financial analyst agent
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
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=create_financial_analyst()
    )


def create_risk_assessment_task(company_data: dict) -> Task:
    """
    Create risk assessment task.

    Args:
        company_data: User input with company details.

    Returns:
        Task object for risk assessor agent
    """
    company_name = company_data.get("company_name", "the company")
    website = company_data.get("website", "")
    
    description = f"""
    Identify catastrophic failure modes and risks for {company_name}.
    
    Company details:
    - Website: {website}
    
    Assessment instructions:
    1. Search for negative signals about the company, founders, or market
    2. Identify top 5 risks with likelihood (1-5) and impact (1-5) scores
    3. Model 2-3 realistic failure scenarios ("How this company fails")
    4. Propose monitoring plan with key metrics to track monthly and red flags to watch
    5. Recommend mitigations for each high-likelihood or high-impact risk
    
    Be paranoid—what could go catastrophically wrong?
    Risk scores 4-5 in likelihood or impact are serious concerns.
    Include regulatory, competitive, execution, and market risks.
    If data unavailable, state "Tool data unavailable" but reason through scenarios.
    """
    
    expected_output = """
    Markdown report with the following sections:
    - **Top 5 Risks:** Table with columns: Risk | Likelihood (1-5) | Impact (1-5) | Mitigation
    - **Failure Scenarios:** 2-3 realistic "How this company fails" narratives
    - **Monitoring Plan:** Key metrics to track monthly and red flags to watch
    """
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=create_risk_assessor()
    )
