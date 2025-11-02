"""
CrewAI Orchestration Service
Coordinates all 8 agents through 17 sequential tasks (5 topic rounds)

Architecture: Independent Round Contexts
- Round 1 (Market): Tasks 1-4, context within round only
- Round 2 (Team): Tasks 5-8, fresh start (no Round 1 context)
- Round 3 (Product): Tasks 9-12, fresh start (no previous rounds)
- Round 4 (Financial): Tasks 13-16, fresh start (no previous rounds)
- Round 5 (Decision): Task 17, sees ALL 16 previous tasks
"""

from crewai import Crew, Process, Task
# TODO: Import when Michael creates these
# from backend.agents.definitions import create_all_agents
# from backend.tasks.debate_tasks import (create task functions)
import asyncio
import uuid
import logging
import json

logger = logging.getLogger(__name__)

class VCCouncilOrchestrator:
    """
    Main orchestrator for VC Council
    Manages 17 sequential tasks through 5 topic-based rounds
    """

    def __init__(self):
        self.sessions = {}  # Store active sessions

    async def start_analysis(self, company_data: dict) -> str:
        """
        Start investment analysis

        Args:
            company_data: Dict with company_name, website, founder_github, etc.

        Returns:
            session_id: Unique ID for this analysis
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "status": "running",
            "company_data": company_data,
            "result": None
        }

        # Run analysis in background
        asyncio.create_task(self._run_analysis(session_id, company_data))

        logger.info(f"Started analysis for {company_data.get('company_name')} (session: {session_id})")
        return session_id

    async def _run_analysis(self, session_id: str, company_data: dict):
        """
        Execute 17 sequential tasks through 5 topic rounds

        Round 1: Market Discussion (Tasks 1-4, independent context)
        Round 2: Team Discussion (Tasks 5-8, fresh start)
        Round 3: Product Discussion (Tasks 9-12, fresh start)
        Round 4: Financial Discussion (Tasks 13-16, fresh start)
        Round 5: Final Decision (Task 17, sees all 16 tasks)
        """
        try:
            logger.info(f"Starting 17-task analysis for {company_data['company_name']}")

            # TODO: Uncomment when Michael creates create_all_agents()
            # agents = create_all_agents()
            # For now, placeholder
            agents = {}

            # ==========================================
            # ROUND 1: MARKET DISCUSSION (Tasks 1-4)
            # Independent context - fresh start
            # ==========================================
            logger.info("Starting Round 1: Market Discussion")

            # Task 1: Market Researcher (context=[])
            # TODO: Uncomment when Michael creates this function
            # task_1 = create_market_researcher_task(agents, company_data, context=[])

            # Task 2: Bull Agent (context=[Task 1])
            # TODO: Uncomment when Michael creates this function
            # task_2 = create_bull_market_task(agents, company_data, context=[task_1])

            # Task 3: Bear Agent (context=[Tasks 1-2])
            # TODO: Uncomment when Michael creates this function
            # task_3 = create_bear_market_task(agents, company_data, context=[task_1, task_2])

            # Task 4: Risk Assessor (context=[Tasks 1-3])
            # TODO: Uncomment when Michael creates this function
            # task_4 = create_risk_market_task(agents, company_data, context=[task_1, task_2, task_3])

            # ==========================================
            # ROUND 2: TEAM DISCUSSION (Tasks 5-8)
            # Independent context - FRESH START (no Round 1!)
            # ==========================================
            logger.info("Starting Round 2: Team Discussion (fresh start)")

            # Task 5: Founder Evaluator (context=[])  ← Fresh start!
            # TODO: Uncomment when Michael creates this function
            # task_5 = create_founder_evaluator_task(agents, company_data, context=[])

            # Task 6: Bull Agent (context=[Task 5])
            # TODO: Uncomment when Michael creates this function
            # task_6 = create_bull_team_task(agents, company_data, context=[task_5])

            # Task 7: Bear Agent (context=[Tasks 5-6])
            # TODO: Uncomment when Michael creates this function
            # task_7 = create_bear_team_task(agents, company_data, context=[task_5, task_6])

            # Task 8: Risk Assessor (context=[Tasks 5-7])
            # TODO: Uncomment when Michael creates this function
            # task_8 = create_risk_team_task(agents, company_data, context=[task_5, task_6, task_7])

            # ==========================================
            # ROUND 3: PRODUCT DISCUSSION (Tasks 9-12)
            # Independent context - FRESH START (no previous rounds!)
            # ==========================================
            logger.info("Starting Round 3: Product Discussion (fresh start)")

            # Task 9: Product Critic (context=[])  ← Fresh start!
            # TODO: Uncomment when Michael creates this function
            # task_9 = create_product_critic_task(agents, company_data, context=[])

            # Task 10: Bull Agent (context=[Task 9])
            # TODO: Uncomment when Michael creates this function
            # task_10 = create_bull_product_task(agents, company_data, context=[task_9])

            # Task 11: Bear Agent (context=[Tasks 9-10])
            # TODO: Uncomment when Michael creates this function
            # task_11 = create_bear_product_task(agents, company_data, context=[task_9, task_10])

            # Task 12: Market Researcher (context=[Tasks 9-11])
            # TODO: Uncomment when Michael creates this function
            # task_12 = create_market_product_task(agents, company_data, context=[task_9, task_10, task_11])

            # ==========================================
            # ROUND 4: FINANCIAL DISCUSSION (Tasks 13-16)
            # Independent context - FRESH START (no previous rounds!)
            # ==========================================
            logger.info("Starting Round 4: Financial Discussion (fresh start)")

            # Task 13: Financial Analyst (context=[])  ← Fresh start!
            # TODO: Uncomment when Michael creates this function
            # task_13 = create_financial_analyst_task(agents, company_data, context=[])

            # Task 14: Bull Agent (context=[Task 13])
            # TODO: Uncomment when Michael creates this function
            # task_14 = create_bull_financial_task(agents, company_data, context=[task_13])

            # Task 15: Bear Agent (context=[Tasks 13-14])
            # TODO: Uncomment when Michael creates this function
            # task_15 = create_bear_financial_task(agents, company_data, context=[task_13, task_14])

            # Task 16: Risk Assessor (context=[Tasks 13-15])
            # TODO: Uncomment when Michael creates this function
            # task_16 = create_risk_financial_task(agents, company_data, context=[task_13, task_14, task_15])

            # ==========================================
            # ROUND 5: FINAL DECISION (Task 17)
            # Sees EVERYTHING - context=[Tasks 1-16]
            # ==========================================
            logger.info("Starting Round 5: Final Decision (sees all 16 tasks)")

            # Task 17: Lead Partner (context=[Tasks 1-16])  ← Full debate history!
            # TODO: Uncomment when Michael creates this function
            # task_17 = create_lead_partner_decision_task(
            #     agents,
            #     company_data,
            #     context=[task_1, task_2, task_3, task_4,      # Round 1
            #              task_5, task_6, task_7, task_8,      # Round 2
            #              task_9, task_10, task_11, task_12,   # Round 3
            #              task_13, task_14, task_15, task_16]  # Round 4
            # )

            # ==========================================
            # CREATE CREW AND RUN
            # ==========================================
            # TODO: Uncomment when Michael creates all 17 task functions
            # all_tasks = [
            #     task_1, task_2, task_3, task_4,      # Round 1: Market
            #     task_5, task_6, task_7, task_8,      # Round 2: Team
            #     task_9, task_10, task_11, task_12,   # Round 3: Product
            #     task_13, task_14, task_15, task_16,  # Round 4: Financial
            #     task_17                              # Round 5: Decision
            # ]
            #
            # crew = Crew(
            #     agents=list(agents.values()),
            #     tasks=all_tasks,
            #     process=Process.sequential,  # Run tasks in order
            #     verbose=True,
            #     step_callback=self._step_callback
            # )
            #
            # logger.info("Starting 17-task sequential debate...")
            #
            # # Run the crew
            # result = await asyncio.to_thread(
            #     crew.kickoff,
            #     inputs=company_data
            # )
            #
            # # Parse and store result
            # decision = json.loads(result) if isinstance(result, str) else result
            #
            # self.sessions[session_id]["status"] = "completed"
            # self.sessions[session_id]["result"] = decision
            #
            # logger.info(f"Analysis completed: {decision.get('decision', 'UNKNOWN')}")

            # Temporary placeholder until Michael creates tasks
            logger.warning("Orchestrator structure ready, waiting for Michael to create task functions")
            self.sessions[session_id]["status"] = "pending_tasks"
            self.sessions[session_id]["message"] = "Waiting for Michael to create 17 task functions"

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            self.sessions[session_id]["status"] = "failed"
            self.sessions[session_id]["error"] = str(e)

    def _step_callback(self, step_output):
        """
        Callback for each agent step
        Broadcasts updates to frontend via SSE (Person 3's responsibility)
        """
        try:
            # Extract agent and message from step output
            agent_name = step_output.get("agent", "unknown")
            message = step_output.get("output", "")

            # TODO: Broadcast to frontend via SSE (Person 3 handles this)
            logger.info(f"[{agent_name}] {message[:100]}...")

        except Exception as e:
            logger.error(f"Step callback error: {str(e)}")

    async def get_result(self, session_id: str) -> dict:
        """Get analysis result by session ID"""
        session = self.sessions.get(session_id)
        if not session:
            return None

        return {
            "session_id": session_id,
            "status": session["status"],
            "company_data": session["company_data"],
            "result": session.get("result"),
            "error": session.get("error"),
            "message": session.get("message")
        }
