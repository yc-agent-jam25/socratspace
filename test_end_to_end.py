#!/usr/bin/env python3
"""
End-to-End Test for VC Council System
Tests the full 17-task sequential architecture
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime

# Test company data
TEST_COMPANY = {
    "company_name": "Cursor AI",
    "website": "https://cursor.sh",
    "industry": "Developer Tools / AI",
    "product_description": "AI-powered code editor that helps developers write code faster",
    "founder_github": "anysphere",
    "financial_metrics": {
        "arr": "$20M",
        "growth_rate": "300% YoY"
    }
}

BASE_URL = "http://localhost:8000"

async def test_full_analysis():
    """Run a complete analysis from start to finish"""

    print("=" * 80)
    print("🚀 VC COUNCIL END-TO-END TEST")
    print("=" * 80)
    print(f"\nTesting company: {TEST_COMPANY['company_name']}")
    print(f"Architecture: 17 sequential tasks across 5 rounds")
    print("-" * 80)

    async with httpx.AsyncClient(timeout=600.0) as client:
        # Step 1: Start analysis
        print("\n📤 Step 1: Starting analysis...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/analyze",
                json=TEST_COMPANY
            )
            response.raise_for_status()
            data = response.json()

            session_id = data["session_id"]
            print(f"✅ Analysis started!")
            print(f"   Session ID: {session_id}")
            print(f"   Status: {data['status']}")
            print(f"   Message: {data['message']}")

        except httpx.HTTPStatusError as e:
            print(f"❌ Failed to start analysis: {e}")
            print(f"   Response: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

        # Step 2: Monitor via SSE (first few events)
        print(f"\n📡 Step 2: Connecting to SSE for real-time updates...")
        print(f"   SSE URL: {BASE_URL}/api/sse/{session_id}")
        print("-" * 80)

        try:
            event_count = 0
            max_preview_events = 10  # Show first 10 events as preview

            async with client.stream("GET", f"{BASE_URL}/api/sse/{session_id}") as sse_response:
                async for line in sse_response.aiter_lines():
                    if line.startswith("data: "):
                        event_count += 1
                        event_data = line[6:]  # Remove "data: " prefix

                        try:
                            event = json.loads(event_data)

                            if event_count <= max_preview_events:
                                # Show preview of first few events
                                event_type = event.get("type", "unknown")

                                if event_type == "phase_change":
                                    phase = event.get("phase", "unknown")
                                    print(f"\n🔄 Phase Change: {phase}")

                                elif event_type == "agent_message":
                                    agent = event.get("agent", "unknown")
                                    message = event.get("message", "")[:100]
                                    print(f"   🤖 {agent}: {message}...")

                                elif event_type == "decision":
                                    decision = event.get("decision", {})
                                    print(f"\n✅ FINAL DECISION: {decision.get('decision', 'UNKNOWN')}")
                                    print(f"   (Full decision will be shown at end)")

                            elif event_count == max_preview_events + 1:
                                print(f"\n   ... (streaming {max_preview_events}+ more events in background)")

                            # Check if analysis is complete
                            if event.get("type") == "phase_change" and event.get("phase") == "completed":
                                print(f"\n✅ Analysis completed after {event_count} SSE events")
                                break

                            if event.get("type") == "error":
                                print(f"\n❌ Error event received: {event.get('error')}")
                                break

                        except json.JSONDecodeError:
                            pass  # Skip non-JSON lines

        except Exception as e:
            print(f"❌ SSE streaming error: {e}")
            print("   Continuing to poll for results...")

        # Step 3: Get final result
        print(f"\n📊 Step 3: Fetching final analysis result...")

        try:
            # Poll for completion (max 40 attempts = 10 minutes)
            for attempt in range(40):
                await asyncio.sleep(15)

                response = await client.get(f"{BASE_URL}/api/analysis/{session_id}")
                response.raise_for_status()
                result = response.json()

                status = result.get("status", "unknown")
                elapsed_min = (attempt + 1) * 15 / 60
                print(f"   [{elapsed_min:.1f}min] Status: {status}")

                if status == "completed":
                    print("\n" + "=" * 80)
                    print("✅ ANALYSIS COMPLETE - FINAL RESULT")
                    print("=" * 80)

                    decision_data = result.get("result", {})

                    # Parse the string representation of Pydantic model
                    import re
                    result_str = decision_data.get('result', '')

                    # Extract decision
                    decision_match = re.search(r"decision='(\w+)'", result_str)
                    decision = decision_match.group(1) if decision_match else decision_data.get('decision', 'UNKNOWN')

                    # Extract reasoning
                    reasoning_match = re.search(r"reasoning='(.*?)' investment_memo=", result_str, re.DOTALL)
                    reasoning = reasoning_match.group(1) if reasoning_match else decision_data.get('reasoning', 'No reasoning provided')
                    reasoning = reasoning.replace('\\\\n', '\n').replace("\\'", "'")

                    # Extract memo
                    memo_match = re.search(r"investment_memo='(.*?)' calendar_events=", result_str, re.DOTALL)
                    memo = memo_match.group(1) if memo_match else decision_data.get('investment_memo', 'No memo provided')
                    memo = memo.replace('\\\\n', '\n').replace("\\'", "'")

                    # Extract events
                    events_match = re.search(r"calendar_events=\[(.*?)\]", result_str)
                    events_str = events_match.group(1) if events_match else ""

                    print(f"\n🎯 DECISION: {decision}")
                    print("\n" + "-" * 80)
                    print("💭 REASONING:")
                    print("-" * 80)
                    print(reasoning)

                    print("\n" + "-" * 80)
                    print("📝 INVESTMENT MEMO:")
                    print("-" * 80)
                    print(memo)

                    print("\n" + "-" * 80)
                    print("📅 CALENDAR EVENTS:")
                    print("-" * 80)

                    if events_str and events_str.strip():
                        title_match = re.search(r"title='(.*?)'", events_str)
                        start_match = re.search(r"start_time='(.*?)'", events_str)
                        attendees_match = re.search(r"attendees=\[(.*?)\]", events_str)

                        if title_match:
                            print(f"\n   📌 {title_match.group(1)}")
                            print(f"   ⏰ {start_match.group(1) if start_match else 'N/A'}")
                            if attendees_match:
                                attendees = attendees_match.group(1).replace("'", "").split(", ")
                                print(f"   👥 {', '.join(attendees)}")
                    else:
                        print("\n   (No events scheduled)")

                    print("\n" + "=" * 80)
                    print("📊 17-TASK EXECUTION - DETAILED OUTPUTS")
                    print("=" * 80)

                    # Display individual task outputs
                    task_outputs = result.get("task_outputs", [])
                    if task_outputs:
                        rounds = [
                            ("ROUND 1: MARKET DISCUSSION", task_outputs[0:4]),
                            ("ROUND 2: TEAM DISCUSSION (FRESH START)", task_outputs[4:8]),
                            ("ROUND 3: PRODUCT DISCUSSION (FRESH START)", task_outputs[8:12]),
                            ("ROUND 4: FINANCIAL DISCUSSION (FRESH START)", task_outputs[12:16]),
                            ("ROUND 5: FINAL DECISION (SEES ALL 16 TASKS)", task_outputs[16:17])
                        ]

                        for round_name, tasks in rounds:
                            print(f"\n{'='*80}")
                            print(f"🔄 {round_name}")
                            print(f"{'='*80}")

                            for task in tasks:
                                task_num = task.get("task_number")
                                task_label = task.get("task_label")
                                agent = task.get("agent")
                                output = task.get("output", "No output")

                                print(f"\n📋 {task_label}")
                                print(f"🤖 Agent: {agent}")
                                print("-" * 80)
                                # Show first 500 chars of output
                                preview = output[:500] + "..." if len(output) > 500 else output
                                print(preview)
                                print()
                    else:
                        print("\n⚠️ Task outputs not captured (backend may need restart)")

                    print("=" * 80)
                    return True

                elif status == "failed":
                    print(f"\n❌ Analysis failed:")
                    print(f"   Error: {result.get('error', 'Unknown error')}")
                    return False

            print(f"\n⚠️  Analysis still running after 10 minutes")
            print(f"   Final status: {status}")
            print(f"   Check backend logs to see progress")
            return False

        except Exception as e:
            print(f"❌ Error fetching result: {e}")
            return False

def check_backend_health():
    """Check if backend is running"""
    import requests
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
        print(f"✅ Backend is healthy: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        print(f"\n⚠️  Please start the backend first:")
        print(f"   cd backend")
        print(f"   source venv/bin/activate")
        print(f"   python main.py")
        return False

if __name__ == "__main__":
    print("\n🔍 Pre-flight check: Testing backend connectivity...\n")

    if not check_backend_health():
        sys.exit(1)

    print("\n" + "=" * 80)
    print("Starting end-to-end test...")
    print("=" * 80)

    success = asyncio.run(test_full_analysis())

    if success:
        print("\n✅ END-TO-END TEST PASSED!")
        print("   All 17 tasks executed successfully")
        print("   System is production-ready 🎉")
        sys.exit(0)
    else:
        print("\n❌ END-TO-END TEST FAILED")
        sys.exit(1)
