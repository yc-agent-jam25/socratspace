"""
Test script for the VC Council agent system.
Executes a full workflow: 5 research tasks → bull → bear → decision.
"""

import json
import sys
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from pathlib import Path

# Load environment variables from backend/.env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Mock mode flag - set to True to skip LLM calls and show mock results
MOCK_MODE = os.getenv('MOCK_MODE', 'false').lower() == 'true'

# Import all agents and tasks
from backend.agents.definitions import create_all_agents
from backend.tasks.research_tasks import (
    create_market_research_task,
    create_founder_evaluation_task,
    create_product_analysis_task,
    create_financial_analysis_task,
    create_risk_assessment_task
)
from backend.tasks.debate_tasks import (
    create_bull_case_task,
    create_bear_case_task
)
from backend.tasks.decision_tasks import create_decision_task


def validate_decision_output(decision_obj) -> dict:
    """
    Validate and convert the decision output to dict.
    
    Args:
        decision_obj: Pydantic model output from the decision task
        
    Returns:
        Dict representation
        
    Raises:
        AssertionError: If output is invalid or missing required keys
    """
    # Convert Pydantic model to dict
    if hasattr(decision_obj, 'model_dump'):
        d = decision_obj.model_dump()
    elif hasattr(decision_obj, 'dict'):
        d = decision_obj.dict()
    else:
        d = dict(decision_obj)
    
    assert d["decision"] in ["PASS", "MAYBE", "INVEST"], f"Invalid decision: {d['decision']}"
    for k in ["reasoning", "investment_memo", "calendar_events"]:
        assert k in d, f"Missing required key: {k}"
    return d


def main():
    """Run the full VC Council workflow."""
    print("=" * 80)
    print("VC Council Agent System - Test Execution")
    print("=" * 80)
    
    # Create minimal company data for testing
    company_data = {
        "company_name": "Acme AI",
        "website": "https://example.com/acme-ai",
        "industry": "AI/ML Automation",
        "product_description": "AI-powered workflow automation platform for enterprise teams",
        "founder_github": "johndoe",  # Optional
        "financial_metrics": {
            "arpu": 150,
            "gross_margin": 0.85,
            "cac": 500,
            "monthly_burn": 50000,
            "active_users": 1000
        }
    }
    
    print(f"\n📊 Company: {company_data['company_name']}")
    print(f"🌐 Website: {company_data['website']}")
    print(f"🏭 Industry: {company_data['industry']}")
    
    # Create all agents
    print("\n🤖 Creating 8 agents...")
    agents = create_all_agents()
    print(f"   ✓ Created {len(agents)} agents")
    assert len(agents) == 8, f"Expected 8 agents, got {len(agents)}"
    
    # Create 5 research tasks
    print("\n📝 Creating 5 research tasks...")
    market_task = create_market_research_task(company_data)
    founder_task = create_founder_evaluation_task(company_data)
    product_task = create_product_analysis_task(company_data)
    financial_task = create_financial_analysis_task(company_data)
    risk_task = create_risk_assessment_task(company_data)
    
    research_tasks = [market_task, founder_task, product_task, financial_task, risk_task]
    print(f"   ✓ Created {len(research_tasks)} research tasks")
    
    # Create bull task
    print("\n🐂 Creating bull case task...")
    bull_task = create_bull_case_task(research_tasks)
    print("   ✓ Created bull task")
    
    # Create bear task
    print("\n🐻 Creating bear case task...")
    bear_task = create_bear_case_task(research_tasks, bull_task)
    print("   ✓ Created bear task")
    
    # Create decision task
    print("\n⚖️  Creating decision task...")
    all_previous = research_tasks + [bull_task, bear_task]
    decision_task = create_decision_task(all_previous, company_data)
    print("   ✓ Created decision task")
    
    # Build crew with all tasks
    print("\n👥 Building Crew...")
    crew = Crew(
        agents=list(agents.values()),
        tasks=research_tasks + [bull_task, bear_task, decision_task],
        process=Process.sequential,
        verbose=True
    )
    print("   ✓ Crew built successfully")
    
    # Execute
    print("\n" + "=" * 80)
    print("🚀 Executing Crew workflow...")
    print("=" * 80)
    
    if MOCK_MODE:
        print("\n⚠️  MOCK MODE ENABLED - Using demo data instead of real LLM calls")
        print("=" * 80)
        # Create mock decision output
        from datetime import datetime, timedelta
        result = {
            "decision": "MAYBE",
            "reasoning": """
            After comprehensive analysis across market, team, product, financials, and risk dimensions, 
            Acme AI presents a **MAYBE** opportunity.
            
            The market for AI/ML automation is substantial and growing, with positive industry sentiment.
            The founding team shows solid technical capabilities (7/10) but has a prior failed venture 
            that raises execution questions. The product is competitively positioned but lacks a strong 
            defensive moat (copyable in 6 months).
            
            Financially, unit economics are reasonable with LTV:CAC at ~2.5:1, showing conservative 
            assumptions. The burn rate is manageable with adequate runway.
            
            However, several risks give pause: intense competition from established players, regulatory 
            uncertainty around AI, and questions around true differentiation in a crowded market.
            
            **Decision Rationale:** This is not a clear PASS due to strong market opportunity and capable 
            team. It's also not a clear INVEST without more validation on customer traction, clearer 
            differentiation, and execution velocity proof. The appropriate decision is MAYBE with a 
            90-day follow-up to assess progress on key milestones.
            """,
            "investment_memo": """
            # Investment Analysis: Acme AI
            
            ## Executive Summary
            Acme AI is developing an AI-powered workflow automation platform for enterprise teams. 
            Analysis indicates a MAYBE decision pending validation of key milestones.
            
            ## Market Opportunity
            - TAM: $73-147B in AI/ML automation sub-segment
            - Market sentiment: Positive with concerns about tool maturity
            - Key competitors: UiPath, Automation Anywhere, Blue Prism
            
            ## Team Assessment
            - Score: 7/10
            - Strong: Technical proficiency, domain expertise
            - Concerns: Prior failed venture, execution velocity uncertainty
            
            ## Product & Competitive Position
            - Moat: Weak (copyable in 6 months)
            - Differentiators: Unclear sustainable advantages
            - Risk: Intense competition, regulatory uncertainty
            
            ## Financial Health
            - LTV:CAC: 2.5:1 (conservative estimates)
            - Burn: $50K/month
            - Runway: Adequate with current metrics
            
            ## Recommendation
            MAYBE - Schedule 90-day follow-up to assess:
            1. Customer traction and PMF signals
            2. Execution velocity improvements
            3. Clearer differentiation strategy
            4. Regulatory position clarification
            """,
            "calendar_events": [
                {
                    "title": "Re-evaluate: Acme AI traction review",
                    "start_time": (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%dT14:00:00'),
                    "end_time": (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%dT15:00:00'),
                    "attendees": ["Partner: Lead Analyst", "IC: Investment Committee"],
                    "description": "Follow-up meeting to reassess progress on key milestones: customer traction, execution velocity, product differentiation, and regulatory clarity."
                }
            ]
        }
        # Convert to Pydantic model for validation
        from backend.tasks.decision_tasks import InvestmentDecision
        result = InvestmentDecision(**result)
    else:
        try:
            result = crew.kickoff()
        except Exception as e:
            print(f"\n❌ Error during execution: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    print("\n" + "=" * 80)
    print("✅ Workflow completed!")
    print("=" * 80)
    
    # Parse and display result
    print("\n📋 Decision Output:")
    print("-" * 80)
    
    try:
        decision_json = validate_decision_output(result)
        print(json.dumps(decision_json, indent=2))
        print("\n✓ Decision output is valid!")
    except (AttributeError, AssertionError) as e:
        print(f"❌ Validation error: {e}")
        print("\nRaw output:")
        print(result)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("🎉 Test completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()

