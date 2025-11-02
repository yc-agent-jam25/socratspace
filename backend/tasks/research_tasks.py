"""
Phase 1: Research Tasks
These run in parallel for maximum speed

TODO: Create 5 research task functions
"""

from crewai import Task
# TODO: Import agent creation functions when ready
# from backend.agents.definitions import (
#     create_market_researcher,
#     create_founder_evaluator,
#     create_product_critic,
#     create_financial_analyst,
#     create_risk_assessor
# )

def create_market_research_task(company_data: dict) -> Task:
    """
    Create market research task

    Args:
        company_data: User input with company_name, website, industry, etc.

    Returns:
        Task object for market researcher agent

    TODO: Implement task with detailed description
    """
    # TODO: Implement
    pass

def create_founder_evaluation_task(company_data: dict) -> Task:
    """
    Create founder evaluation task

    TODO: Implement task for analyzing founders via GitHub
    """
    # TODO: Implement
    pass

def create_product_analysis_task(company_data: dict) -> Task:
    """
    Create product and moat analysis task

    TODO: Implement task for defensibility analysis
    """
    # TODO: Implement
    pass

def create_financial_analysis_task(company_data: dict) -> Task:
    """
    Create financial analysis task

    TODO: Implement task for unit economics analysis
    """
    # TODO: Implement
    pass

def create_risk_assessment_task(company_data: dict) -> Task:
    """
    Create risk assessment task

    TODO: Implement task for identifying risks and red flags
    """
    # TODO: Implement
    pass
