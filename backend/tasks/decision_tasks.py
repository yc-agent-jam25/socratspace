"""
Phase 5: Decision Task
Lead Partner makes final investment decision (PASS/MAYBE/INVEST) based on all evidence.
"""

from crewai import Task
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import List, Literal
from backend.agents.definitions import create_lead_partner


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


def create_decision_task(all_previous_tasks: list, company_data: dict) -> Task:
    """
    Create decision-making task for Lead Partner.

    Args:
        all_previous_tasks: All research + debate tasks
        company_data: Original company info

    Returns:
        Task object that outputs JSON with decision
    """
    company_name = company_data.get("company_name", "this company")
    
    # Calculate key dates for calendar events
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    two_weeks = today + timedelta(days=14)
    three_months = today + timedelta(days=90)
    
    description = f"""
    Make the final investment decision for {company_name}.
    
    You have access to ALL previous analysis:
    - Market Research: TAM, growth, competitors, sentiment
    - Founder Evaluation: Team quality, execution, red flags
    - Product Analysis: Moat, defensibility, competitive threats
    - Financial Analysis: LTV:CAC, burn, runway, health score
    - Risk Assessment: Top risks, failure scenarios, mitigations
    - Bull Case: Investment thesis, reasons to invest, upside potential
    - Bear Case: Counter-thesis, reasons not to invest, downside risks, rebuttals
    
    Your mission: Synthesize all arguments and make a decisive PASS/MAYBE/INVEST decision.
    
    Decision Framework:
    - **PASS:** Fundamental flaws, insurmountable risks, or weak team/product
    - **MAYBE:** Promising but needs validation (user traction, key hires, milestones)
    - **INVEST:** Strong opportunity with compelling team, market, product, and economics
    
    Process:
    1. Weigh all research findings objectively
    2. Consider Bull's arguments for investing and Bear's arguments against
    3. Balance both sides rigorously—neither follow hype nor paralyze with fear
    4. Make decisive decision (PASS/MAYBE/INVEST) with clear reasoning
    5. Generate investment memo and calendar events based on decision
    
    Calendar Event Rules:
    - **PASS:** calendar_events = [] (empty array, no events)
    - **MAYBE:** One follow-up event in ~90 days (e.g., "Re-evaluate: {company_name} traction review")
      - Start time: {three_months.strftime('%Y-%m-%dT14:00:00')}
      - End time: {three_months.strftime('%Y-%m-%dT15:00:00')}
    - **INVEST:** 2-3 events within 14 days:
      1. Due diligence kickoff: {tomorrow.strftime('%Y-%m-%dT14:00:00')} (tomorrow)
      2. IC/Partner meeting: {next_week.strftime('%Y-%m-%dT14:00:00')} (within 7 days)
      3. Term sheet negotiation: {two_weeks.strftime('%Y-%m-%dT14:00:00')} (within 14 days)
    
    CRITICAL: Your output MUST be valid JSON parseable by json.loads().
    Use this EXACT structure (no markdown, no extra text):
    {{
      "decision": "PASS | MAYBE | INVEST",
      "reasoning": "3-5 paragraph explanation weighing both sides",
      "investment_memo": "Comprehensive memo summarizing key findings and recommendation",
      "calendar_events": [
        {{
          "title": "Event title",
          "start_time": "ISO8601 datetime",
          "end_time": "ISO8601 datetime",
          "attendees": ["array of strings"],
          "description": "Event description"
        }}
      ]
    }}
    
    Attendees format: ["Partner: Sarah Chen", "IC: Michael Park"] or similar specific names/titles.
    """
    
    expected_output = """
    Valid structured output with these fields:
    - decision: "PASS" | "MAYBE" | "INVEST"
    - reasoning: 3-5 paragraph explanation of decision weighing both sides
    - investment_memo: Comprehensive memo summarizing key findings and recommendation
    - calendar_events: Array of event objects or empty array based on decision
    """
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=create_lead_partner(),
        context=all_previous_tasks,
        output_pydantic=InvestmentDecision
    )
