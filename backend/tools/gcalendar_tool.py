"""
Google Calendar Tool
Creates calendar events for investment follow-ups via Metorial Google Calendar MCP
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Optional
from tools.mcp_client import mcp_client
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class CalendarEventInput(BaseModel):
    """Input schema for calendar event creation"""
    title: str = Field(..., description="Event title/name")
    start_time: str = Field(..., description="Event start time (ISO format: YYYY-MM-DDTHH:MM:SS or natural language)")
    duration_minutes: Optional[int] = Field(
        default=60,
        description="Event duration in minutes (default: 60)"
    )
    description: Optional[str] = Field(
        default=None,
        description="Event description/details"
    )
    attendees: Optional[List[str]] = Field(
        default=None,
        description="List of attendee email addresses"
    )
    location: Optional[str] = Field(
        default=None,
        description="Event location"
    )

class GoogleCalendarTool(BaseTool):
    """
    Google Calendar event creation tool for investment follow-ups
    """
    name: str = "Google Calendar"
    description: str = """
    Creates calendar events in Google Calendar for investment follow-ups and meetings.

    Use this tool to:
    - Schedule due diligence meetings
    - Create follow-up reminders
    - Schedule partner meetings
    - Set up term sheet negotiations
    - Create calendar events for investment milestones

    Requires: Google Calendar OAuth authentication (automatically handled).

    Input: Event details including title, start time, duration, attendees, description.
    Returns: Confirmation of created events with event IDs and links.
    """
    args_schema: Type[BaseModel] = CalendarEventInput

    def _run(
        self,
        title: str,
        start_time: str,
        duration_minutes: int = 60,
        description: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        location: Optional[str] = None
    ) -> str:
        """
        Create a calendar event via Metorial Google Calendar MCP

        Args:
            title: Event title
            start_time: Event start time (ISO format or natural language)
            duration_minutes: Event duration in minutes
            description: Event description
            attendees: List of attendee email addresses
            location: Event location

        Returns:
            Formatted string with event creation confirmation
        """

        async def create_event():
            try:
                logger.info(f"Creating calendar event: {title} at {start_time}")

                # Prepare event parameters
                event_params = {
                    "title": title,
                    "start_time": start_time,
                    "duration_minutes": duration_minutes,
                }

                if description:
                    event_params["description"] = description
                if attendees:
                    event_params["attendees"] = attendees
                if location:
                    event_params["location"] = location

                # Call MCP via Metorial with direct action command
                # Use imperative language to trigger actual event creation, not explanations
                result = await mcp_client.call_mcp(
                    mcp_name="gcalendar",
                    tool_name="create_calendar_event",  # For logging only
                    parameters=event_params,
                    natural_message=f"""
                    You have access to Google Calendar MCP tools through this server deployment.
                    DO NOT describe what you would do - USE THE ACTUAL TOOLS AVAILABLE TO YOU NOW.
                    
                    REQUIRED ACTION:
                    1. Look at the available Google Calendar MCP tools in this server deployment
                    2. Find and USE a calendar event creation tool
                    3. Call that tool RIGHT NOW with these event details:
                       - Title: {title}
                       - Start Time: {start_time}
                       - Duration: {duration_minutes} minutes
                       {f"- Description: {description}" if description else ""}
                       {f"- Attendees: {', '.join(attendees)}" if attendees else ""}
                       {f"- Location: {location}" if location else ""}
                    4. Wait for the tool to execute and create the REAL calendar event
                    5. Return the ACTUAL event details that were created (event ID, link, etc.)
                    
                    CRITICAL: You MUST call the actual Google Calendar MCP tools available to you.
                    DO NOT return descriptions, instructions, or explanations.
                    ONLY return the actual event creation confirmation and details from Google Calendar.
                    
                    If you cannot find the tools, list all available tools first, then use one to create the event.
                    """
                )

                # Extract text from RunResult
                calendar_content = result.text

                # Format for LLM consumption
                formatted = f"""
=== Google Calendar Event Created ===
Title: {title}
Start Time: {start_time}
Duration: {duration_minutes} minutes
{f"Description: {description}" if description else ""}
{f"Attendees: {', '.join(attendees)}" if attendees else "No attendees specified"}
{f"Location: {location}" if location else ""}

Result:
{calendar_content}

=== End of Calendar Event ===
"""
                logger.info(f"Calendar event created successfully: {title}")
                return formatted

            except Exception as e:
                error_msg = f"Error creating calendar event '{title}': {str(e)}"
                logger.error(error_msg)
                return f"❌ {error_msg}\n\nNote: Google Calendar OAuth may need to be re-authenticated or check event details."

        return asyncio.run(create_event())

    async def _arun(
        self,
        title: str,
        start_time: str,
        duration_minutes: int = 60,
        description: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        location: Optional[str] = None
    ) -> str:
        """
        Async version of _run for use in async contexts (e.g., FastAPI event loop)
        
        Create a calendar event via Metorial Google Calendar MCP
        
        Args:
            title: Event title
            start_time: Event start time (ISO format or natural language)
            duration_minutes: Event duration in minutes
            description: Event description
            attendees: List of attendee email addresses
            location: Event location
        
        Returns:
            Formatted string with event creation confirmation
        """
        try:
            logger.info(f"Creating calendar event: {title} at {start_time}")

            # Prepare event parameters
            event_params = {
                "title": title,
                "start_time": start_time,
                "duration_minutes": duration_minutes,
            }

            if description:
                event_params["description"] = description
            if attendees:
                event_params["attendees"] = attendees
            if location:
                event_params["location"] = location

            # Call MCP via Metorial with direct action command
            # Use imperative language to trigger actual event creation, not explanations
            result = await mcp_client.call_mcp(
                mcp_name="gcalendar",
                tool_name="create_calendar_event",  # For logging only
                parameters=event_params,
                natural_message=f"""
                You have access to Google Calendar MCP tools through this server deployment.
                DO NOT describe what you would do - USE THE ACTUAL TOOLS AVAILABLE TO YOU NOW.
                
                REQUIRED ACTION:
                1. Look at the available Google Calendar MCP tools in this server deployment
                2. Find and USE a calendar event creation tool
                3. Call that tool RIGHT NOW with these event details:
                   - Title: {title}
                   - Start Time: {start_time}
                   - Duration: {duration_minutes} minutes
                   {f"- Description: {description}" if description else ""}
                   {f"- Attendees: {', '.join(attendees)}" if attendees else ""}
                   {f"- Location: {location}" if location else ""}
                4. Wait for the tool to execute and create the REAL calendar event
                5. Return the ACTUAL event details that were created (event ID, link, etc.)
                
                CRITICAL: You MUST call the actual Google Calendar MCP tools available to you.
                DO NOT return descriptions, instructions, or explanations.
                ONLY return the actual event creation confirmation and details from Google Calendar.
                
                If you cannot find the tools, list all available tools first, then use one to create the event.
                """
            )

            # Extract text from RunResult
            calendar_content = result.text

            # Format for LLM consumption
            formatted = f"""
=== Google Calendar Event Created ===
Title: {title}
Start Time: {start_time}
Duration: {duration_minutes} minutes
{f"Description: {description}" if description else ""}
{f"Attendees: {', '.join(attendees)}" if attendees else "No attendees specified"}
{f"Location: {location}" if location else ""}

Result:
{calendar_content}

=== End of Calendar Event ===
"""
            logger.info(f"Calendar event created successfully: {title}")
            return formatted

        except Exception as e:
            error_msg = f"Error creating calendar event '{title}': {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}\n\nNote: Google Calendar OAuth may need to be re-authenticated or check event details."
