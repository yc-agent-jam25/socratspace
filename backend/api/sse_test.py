"""
Mock SSE endpoint for testing frontend SSE integration
Generates realistic mock events without requiring full backend implementation
"""

import asyncio
import json
from fastapi import Request
from fastapi.responses import StreamingResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def generate_mock_events(session_id: str, request: Request):
    """
    Generate mock SSE events for testing
    Simulates a full analysis flow: research → debate → decision
    """
    
    # IMPORTANT: Send initial connection message immediately
    # EventSource needs data immediately to establish connection
    yield f"data: {json.dumps({'type': 'connected', 'data': {'session_id': session_id}})}\n\n"
    
    # Flush immediately (FastAPI does this automatically, but just to be safe)
    # Small delay to ensure connection is established
    await asyncio.sleep(0.1)
    
    # Phase 1: Research Phase
    yield f"data: {json.dumps({'type': 'phase_change', 'data': {'phase': 'research', 'timestamp': datetime.now().isoformat()}})}\n\n"
    await asyncio.sleep(0.3)
    
    # Research agent messages
    research_messages = [
        ("market_researcher", "Analyzing Total Addressable Market (TAM)...", "analysis"),
        ("founder_evaluator", "Evaluating founder GitHub profile...", "analysis"),
        ("product_critic", "Evaluating product defensibility...", "analysis"),
        ("financial_analyst", "Analyzing unit economics...", "analysis"),
        ("risk_assessor", "Identifying potential risks...", "analysis"),
        ("market_researcher", "TAM estimated at $5.2B with 30% YoY growth.", "insight"),
        ("founder_evaluator", "Founder has 127 repositories, strong ML/AI focus.", "insight"),
        ("product_critic", "Product has strong network effects and proprietary datasets.", "insight"),
        ("financial_analyst", "LTV:CAC ratio of 5.2:1 (healthy). Current burn rate: $85K/month.", "insight"),
        ("risk_assessor", "Top risks: Regulatory uncertainty, Competition, Talent acquisition.", "insight"),
        ("market_researcher", "Market sentiment on HackerNews is highly positive (89%).", "conclusion"),
        ("founder_evaluator", "Team execution score: 9/10. Strong technical background.", "conclusion"),
        ("product_critic", "Product-market fit signals: 12 enterprise pilots, 4 signed LOIs.", "conclusion"),
        ("financial_analyst", "Financial health score: 8/10. Strong unit economics.", "conclusion"),
        ("risk_assessor", "Risk severity: MEDIUM. Manageable with proper execution.", "conclusion"),
    ]
    
    for agent_id, message, message_type in research_messages:
        if await request.is_disconnected():
            return
        
        yield f"data: {json.dumps({
            'type': 'agent_message',
            'data': {
                'agent': agent_id,
                'message': message,
                'message_type': message_type,
                'timestamp': int(datetime.now().timestamp() * 1000)
            }
        })}\n\n"
        
        # Stagger messages for realism
        await asyncio.sleep(0.5)
    
    # Phase 2: Debate Phase
    await asyncio.sleep(1)
    yield f"data: {json.dumps({'type': 'phase_change', 'data': {'phase': 'debate', 'timestamp': datetime.now().isoformat()}})}\n\n"
    await asyncio.sleep(0.3)
    
    # Debate agent messages
    debate_messages = [
        ("bull_agent", "Building the bull case...", "analysis"),
        ("bull_agent", "🐂 STRONG BUY: Market growing 30% YoY, exceptional team with Google/DeepMind background, proven product-market fit.", "insight"),
        ("bear_agent", "Building the bear case...", "analysis"),
        ("bear_agent", "🐻 CAUTION: Only 14 months runway, 60% revenue concentration risk, facing well-funded competition.", "insight"),
        ("bull_agent", "Upside potential: 10x in 3 years. Enterprise AI safety is a $50B+ market by 2028.", "conclusion"),
        ("bear_agent", "Regulatory uncertainty could kill the market. OpenAI and Anthropic entering with 100x more resources.", "conclusion"),
        ("bull_agent", "This team can execute. Strong unit economics (LTV:CAC 5.2:1) and clear path to profitability.", "conclusion"),
        ("bear_agent", "Valuation risk: At current traction, difficult to justify post-money valuation expectations.", "conclusion"),
    ]
    
    for agent_id, message, message_type in debate_messages:
        if await request.is_disconnected():
            return
        
        yield f"data: {json.dumps({
            'type': 'agent_message',
            'data': {
                'agent': agent_id,
                'message': message,
                'message_type': message_type,
                'timestamp': int(datetime.now().timestamp() * 1000)
            }
        })}\n\n"
        
        await asyncio.sleep(0.6)
    
    # Phase 3: Decision Phase
    await asyncio.sleep(1)
    yield f"data: {json.dumps({'type': 'phase_change', 'data': {'phase': 'decision', 'timestamp': datetime.now().isoformat()}})}\n\n"
    await asyncio.sleep(0.3)
    
    # Lead Partner messages
    decision_messages = [
        ("lead_partner", "Synthesizing all arguments...", "analysis"),
        ("lead_partner", "Weighing bull vs bear cases against research findings...", "insight"),
        ("lead_partner", "Final decision reached. Generating investment memo...", "conclusion"),
    ]
    
    for agent_id, message, message_type in decision_messages:
        if await request.is_disconnected():
            return
        
        yield f"data: {json.dumps({
            'type': 'agent_message',
            'data': {
                'agent': agent_id,
                'message': message,
                'message_type': message_type,
                'timestamp': int(datetime.now().timestamp() * 1000)
            }
        })}\n\n"
        
        await asyncio.sleep(1)
    
    # Final Decision
    await asyncio.sleep(1)
    decision = {
        "decision": "INVEST",
        "reasoning": "Strong market opportunity with proven team and product-market fit. Risks are manageable with proper execution.",
        "investment_memo": """# Investment Memo: Test Company

## Executive Summary

Test Company demonstrates strong product-market fit with enterprise pilots and growing MRR. The founding team brings exceptional credentials.

**Recommendation: INVEST** with conditions on extending runway and diversifying customer base.

## Market Opportunity

- **TAM**: $5.2B, growing at 30% YoY
- **Market Position**: Early mover in enterprise segment
- **Competitive Landscape**: 3 major competitors, but significant white space

## Team Assessment

**Strengths:**
- Founders: Ex-Google Brain and DeepMind engineers
- Published 8 papers on AI alignment
- Strong technical background

## Financial Analysis

- **Unit Economics**: LTV:CAC 5.2:1 (healthy)
- **Burn Rate**: $85K/month with 14 months runway
- **MRR**: $42K, growing 25% MoM

## Risks

1. Regulatory uncertainty in AI safety
2. Competition from well-funded players
3. Limited runway (14 months)

## Recommendation

**INVEST** with the following conditions:
1. Extend runway to 18+ months
2. Diversify customer base (reduce concentration risk)
3. Accelerate enterprise sales

## Next Steps

1. Due diligence kickoff meeting
2. Partner meeting to review terms
3. Term sheet negotiation""",
        "calendar_events": [
            {
                "title": "Due Diligence Kickoff",
                "start_time": (datetime.now().replace(hour=10, minute=0, second=0, microsecond=0).isoformat()),
                "end_time": (datetime.now().replace(hour=11, minute=0, second=0, microsecond=0).isoformat()),
                "attendees": ["Lead Partner", "Market Researcher", "Financial Analyst"],
                "description": "Initial due diligence meeting to review company documents"
            },
            {
                "title": "Partner Meeting - Investment Review",
                "start_time": (datetime.now().replace(hour=14, minute=0, second=0, microsecond=0).isoformat()),
                "end_time": (datetime.now().replace(hour=15, minute=30, second=0, microsecond=0).isoformat()),
                "attendees": ["All Partners", "Legal Team"],
                "description": "Review investment decision and discuss terms"
            },
            {
                "title": "Term Sheet Negotiation",
                "start_time": ((datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)).isoformat()),
                "end_time": ((datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)).isoformat()),
                "attendees": ["Lead Partner", "Legal Team", "Founders"],
                "description": "Finalize term sheet and investment structure"
            }
        ]
    }
    
    yield f"data: {json.dumps({'type': 'decision', 'data': decision})}\n\n"
    
    # Mark as completed
    await asyncio.sleep(0.5)
    yield f"data: {json.dumps({'type': 'phase_change', 'data': {'phase': 'completed', 'timestamp': datetime.now().isoformat()}})}\n\n"
    
    # Close connection gracefully after completion
    # EventSource will detect the closure, but frontend will know it's a normal completion
    # No need to keep connection open - frontend has all the data


def create_test_sse_endpoint(session_id: str, request: Request):
    """
    Create SSE test endpoint that generates mock events
    """
    event_generator = generate_mock_events(session_id, request)
    
    # Get origin from request for CORS
    origin = request.headers.get("origin", "*")
    
    return StreamingResponse(
        event_generator,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": origin if origin else "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Cache-Control",
        }
    )

