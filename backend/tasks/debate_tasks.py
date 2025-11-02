"""
Phase 3: Debate Tasks
Bull and Bear agents argue opposite sides

TODO: Create bull and bear case tasks
"""

from crewai import Task
# TODO: Import agent creation functions when ready
# from backend.agents.definitions import create_bull_agent, create_bear_agent

def create_bull_case_task(research_tasks: list) -> Task:
    """
    Create Bull agent task to make case FOR investing

    Args:
        research_tasks: List of 5 research Task objects

    Returns:
        Task object that gets access to all research via context

    TODO: Implement task with:
    - Description: Review research, make strongest bull case
    - Agent: Bull agent
    - Context: research_tasks (this gives access to findings)
    - Expected output: Bull case with thesis, reasons, upside
    """
    # TODO: Implement
    pass

def create_bear_case_task(research_tasks: list, bull_task: Task) -> Task:
    """
    Create Bear agent task to make case AGAINST investing

    Args:
        research_tasks: List of 5 research Task objects
        bull_task: Bull agent's task (Bear can see Bull's arguments)

    Returns:
        Task object that gets access to research + bull case

    TODO: Implement task with:
    - Description: Review research + Bull's argument, make bear case
    - Agent: Bear agent
    - Context: research_tasks + [bull_task]
    - Expected output: Bear case with counter-thesis, risks, counterarguments
    """
    # TODO: Implement
    pass
