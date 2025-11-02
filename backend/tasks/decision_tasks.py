"""
Phase 5: Decision Task
Lead Partner makes final investment decision

TODO: Create decision task
"""

from crewai import Task
from datetime import datetime, timedelta
# TODO: Import agent creation function when ready
# from backend.agents.definitions import create_lead_partner

def create_decision_task(all_previous_tasks: list, company_data: dict) -> Task:
    """
    Create decision-making task for Lead Partner

    Args:
        all_previous_tasks: All research + debate tasks
        company_data: Original company info

    Returns:
        Task object that outputs JSON with decision

    TODO: Implement task with:
    - Description: Synthesize all arguments, make final decision (PASS/MAYBE/INVEST)
    - Agent: Lead Partner
    - Context: all_previous_tasks (sees everything)
    - Expected output: JSON with decision, reasoning, memo, calendar_events
    - output_json=True: CrewAI will parse output as JSON

    Calendar event logic:
    - PASS: []
    - MAYBE: One 3-month follow-up event
    - INVEST: Three events (DD kickoff tomorrow, partner meeting next week, term sheet in 2 weeks)
    """
    # TODO: Implement
    # Calculate dates
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    two_weeks = today + timedelta(days=14)
    three_months = today + timedelta(days=90)

    # TODO: Create task
    pass
