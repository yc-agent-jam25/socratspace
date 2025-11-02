"""
Test Google Calendar Tool
Test creating a calendar event

Note: Google Calendar requires OAuth authentication. This test will:
1. Automatically create an OAuth session
2. Display a URL for you to authenticate
3. Wait for you to complete authentication
4. Then proceed with creating a test calendar event

Usage:
    python test_gcalendar_tool.py

Prerequisites:
    - METORIAL_API_KEY in .env (valid key, not placeholder)
    - OPENAI_API_KEY in .env (valid key starting with sk-)
    - MCP_GCALENDAR_ID in .env (from Metorial dashboard)
"""

from tools.gcalendar_tool import GoogleCalendarTool
from datetime import datetime, timedelta

def test_gcalendar_create_event():
    """Test creating a calendar event"""

    print("=" * 60)
    print("Testing Google Calendar Tool")
    print("=" * 60)
    print("\n⚠️  Note: Google Calendar requires OAuth authentication.")
    print("   You will be prompted to authenticate when the test runs.\n")

    # Create tool instance
    tool = GoogleCalendarTool()

    # Create a test event (tomorrow at 2pm)
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
    start_time_str = start_time.isoformat()

    title = "Test Calendar Event - VC Council Demo"
    print(f"📅 Test: Creating calendar event")
    print("-" * 60)
    print(f"Title: {title}")
    print(f"Start Time: {start_time_str}")
    print(f"Duration: 60 minutes")
    print(f"Description: Test event created by VC Council tool")
    print("\nNote: OAuth flow will start automatically if needed...\n")

    try:
        result = tool._run(
            title=title,
            start_time=start_time_str,
            duration_minutes=60,
            description="Test event created by VC Council tool to verify Google Calendar integration",
            attendees=None,  # Optional
            location=None   # Optional
        )

        # Check if result indicates an error
        if "❌" in result or "error" in result.lower() or "failed" in result.lower():
            print("\n❌ TEST FAILED - Error detected in result!")
            print("\nResult:")
            print(result)
        else:
            print("\n✅ SUCCESS!")
            print("\nResult:")
            print(result)

    except Exception as e:
        print(f"\n❌ FAILED!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_gcalendar_create_event()

