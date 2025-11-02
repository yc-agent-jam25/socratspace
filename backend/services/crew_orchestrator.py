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
from backend.agents.definitions import create_all_agents
from backend.api.sse import sse_manager

# Task imports - your friend is working on these
# Will be available once task functions are created
try:
    from backend.tasks.research_tasks import (
        create_market_researcher_task,
        create_founder_evaluator_task,
        create_product_critic_task,
        create_financial_analyst_task
    )
    from backend.tasks.debate_tasks import (
        create_bull_market_task,
        create_bear_market_task,
        create_bull_team_task,
        create_bear_team_task,
        create_bull_product_task,
        create_bear_product_task,
        create_bull_financial_task,
        create_bear_financial_task
    )
    from backend.tasks.decision_tasks import (
        create_risk_market_task,
        create_risk_team_task,
        create_risk_financial_task,
        create_market_product_task,
        create_lead_partner_decision_task
    )
    TASKS_AVAILABLE = True
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"Task modules not yet available: {e}")
    TASKS_AVAILABLE = False

import asyncio
import uuid
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class VCCouncilOrchestrator:
    """
    Main orchestrator for VC Council
    Manages 17 sequential tasks through 5 topic-based rounds
    """

    def __init__(self):
        self.sessions = {}  # Store active sessions
        self.task_to_agent_map = {}  # Map session_id -> list of agent role names (one per task, 17 total)
        self.current_task_index = {}  # Map session_id -> current task index (0-16)

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
        # Get the current event loop for thread-safe async callbacks
        loop = asyncio.get_running_loop()

        try:
            logger.info(f"Starting 17-task analysis for {company_data['company_name']}")

            # Wait briefly for SSE client to connect (avoid race condition)
            logger.info(f"Waiting for SSE client to connect for session {session_id}...")
            await asyncio.sleep(1.5)  # Give frontend time to establish SSE connection

            # Send starting message via SSE
            await sse_manager.send_phase_change(session_id, "initializing")
            await sse_manager.send_agent_message(
                session_id,
                "system",
                f"Starting analysis for {company_data.get('company_name', 'Unknown Company')}",
                "info"
            )

            # Create all 8 agents
            logger.info("Creating 8 agents...")
            agents = create_all_agents()
            logger.info(f"Agents created: {list(agents.keys())}")

            # Check if tasks are available
            if not TASKS_AVAILABLE:
                logger.warning("Task functions not yet available - waiting for friend to complete")
                await sse_manager.send_error(
                    session_id,
                    "Task functions are being implemented. Please wait for completion.",
                    "TASKS_NOT_READY"
                )
                self.sessions[session_id]["status"] = "pending_tasks"
                self.sessions[session_id]["message"] = "Waiting for task implementations"
                return

            # ==========================================
            # ROUND 1: MARKET DISCUSSION (Tasks 1-4)
            # Independent context - fresh start
            # ==========================================
            logger.info("Starting Round 1: Market Discussion")
            await sse_manager.send_phase_change(session_id, "market_discussion")

            # Task 1: Market Researcher (context=[])
            task_1 = create_market_researcher_task(agents, company_data, context=[])

            # Task 2: Bull Agent (context=[Task 1])
            task_2 = create_bull_market_task(agents, company_data, context=[task_1])

            # Task 3: Bear Agent (context=[Tasks 1-2])
            task_3 = create_bear_market_task(agents, company_data, context=[task_1, task_2])

            # Task 4: Risk Assessor (context=[Tasks 1-3])
            task_4 = create_risk_market_task(agents, company_data, context=[task_1, task_2, task_3])

            # ==========================================
            # ROUND 2: TEAM DISCUSSION (Tasks 5-8)
            # Independent context - FRESH START (no Round 1!)
            # ==========================================
            logger.info("Starting Round 2: Team Discussion (fresh start)")
            await sse_manager.send_phase_change(session_id, "team_discussion")

            # Task 5: Founder Evaluator (context=[])  ← Fresh start!
            task_5 = create_founder_evaluator_task(agents, company_data, context=[])

            # Task 6: Bull Agent (context=[Task 5])
            task_6 = create_bull_team_task(agents, company_data, context=[task_5])

            # Task 7: Bear Agent (context=[Tasks 5-6])
            task_7 = create_bear_team_task(agents, company_data, context=[task_5, task_6])

            # Task 8: Risk Assessor (context=[Tasks 5-7])
            task_8 = create_risk_team_task(agents, company_data, context=[task_5, task_6, task_7])

            # ==========================================
            # ROUND 3: PRODUCT DISCUSSION (Tasks 9-12)
            # Independent context - FRESH START (no previous rounds!)
            # ==========================================
            logger.info("Starting Round 3: Product Discussion (fresh start)")
            await sse_manager.send_phase_change(session_id, "product_discussion")

            # Task 9: Product Critic (context=[])  ← Fresh start!
            task_9 = create_product_critic_task(agents, company_data, context=[])

            # Task 10: Bull Agent (context=[Task 9])
            task_10 = create_bull_product_task(agents, company_data, context=[task_9])

            # Task 11: Bear Agent (context=[Tasks 9-10])
            task_11 = create_bear_product_task(agents, company_data, context=[task_9, task_10])

            # Task 12: Market Researcher (context=[Tasks 9-11])
            task_12 = create_market_product_task(agents, company_data, context=[task_9, task_10, task_11])

            # ==========================================
            # ROUND 4: FINANCIAL DISCUSSION (Tasks 13-16)
            # Independent context - FRESH START (no previous rounds!)
            # ==========================================
            logger.info("Starting Round 4: Financial Discussion (fresh start)")
            await sse_manager.send_phase_change(session_id, "financial_discussion")

            # Task 13: Financial Analyst (context=[])  ← Fresh start!
            task_13 = create_financial_analyst_task(agents, company_data, context=[])

            # Task 14: Bull Agent (context=[Task 13])
            task_14 = create_bull_financial_task(agents, company_data, context=[task_13])

            # Task 15: Bear Agent (context=[Tasks 13-14])
            task_15 = create_bear_financial_task(agents, company_data, context=[task_13, task_14])

            # Task 16: Risk Assessor (context=[Tasks 13-15])
            task_16 = create_risk_financial_task(agents, company_data, context=[task_13, task_14, task_15])

            # ==========================================
            # ROUND 5: FINAL DECISION (Task 17)
            # Sees EVERYTHING - context=[Tasks 1-16]
            # ==========================================
            logger.info("Starting Round 5: Final Decision (sees all 16 tasks)")
            await sse_manager.send_phase_change(session_id, "final_decision")

            # Task 17: Lead Partner (context=[Tasks 1-16])  ← Full debate history!
            task_17 = create_lead_partner_decision_task(
                agents,
                company_data,
                context=[task_1, task_2, task_3, task_4,      # Round 1
                         task_5, task_6, task_7, task_8,      # Round 2
                         task_9, task_10, task_11, task_12,   # Round 3
                         task_13, task_14, task_15, task_16]  # Round 4
            )

            # ==========================================
            # CREATE CREW AND RUN
            # ==========================================
            all_tasks = [
                task_1, task_2, task_3, task_4,      # Round 1: Market
                task_5, task_6, task_7, task_8,      # Round 2: Team
                task_9, task_10, task_11, task_12,   # Round 3: Product
                task_13, task_14, task_15, task_16,  # Round 4: Financial
                task_17                              # Round 5: Decision
            ]

            logger.info(f"Created {len(all_tasks)} sequential tasks")

            # ==========================================
            # BUILD TASK-TO-AGENT MAPPING
            # Extract agent role from each task for step_callback attribution
            # ==========================================
            task_agent_map = []
            for i, task in enumerate(all_tasks):
                agent_role = task.agent.role if hasattr(task, 'agent') and hasattr(task.agent, 'role') else "unknown"
                task_agent_map.append(agent_role)
                logger.info(f"Task {i+1} mapped to agent: {agent_role}")

            # Store mapping for this session
            self.task_to_agent_map[session_id] = task_agent_map
            self.current_task_index[session_id] = 0  # Start at task 0
            logger.info(f"✅ Task-to-agent mapping created for session {session_id}: {len(task_agent_map)} tasks mapped")

            # Create crew with thread-safe callbacks for SSE broadcasting
            def step_callback_sync(step_output):
                """Thread-safe wrapper for async step callback (agent activity)"""
                asyncio.run_coroutine_threadsafe(
                    self._step_callback(session_id, step_output),
                    loop
                )

            crew = Crew(
                agents=list(agents.values()),
                tasks=all_tasks,
                process=Process.sequential,  # Run tasks in order
                verbose=True,
                step_callback=step_callback_sync
            )

            logger.info("Starting 17-task sequential debate...")
            await sse_manager.send_agent_message(
                session_id,
                "system",
                "Initiating 17-task investment analysis with 8 AI agents",
                "info"
            )

            # Run the crew (blocking, so use asyncio.to_thread)
            result = await asyncio.to_thread(
                crew.kickoff,
                inputs=company_data
            )

            # Capture individual task outputs
            task_outputs = []
            task_labels = [
                "Task 1: Market Researcher",
                "Task 2: Bull - Market",
                "Task 3: Bear - Market",
                "Task 4: Risk Assessor - Market",
                "Task 5: Founder Evaluator",
                "Task 6: Bull - Team",
                "Task 7: Bear - Team",
                "Task 8: Risk Assessor - Team",
                "Task 9: Product Critic",
                "Task 10: Bull - Product",
                "Task 11: Bear - Product",
                "Task 12: Market Researcher - PMF",
                "Task 13: Financial Analyst",
                "Task 14: Bull - Financial",
                "Task 15: Bear - Financial",
                "Task 16: Risk Assessor - Financial",
                "Task 17: Lead Partner Decision"
            ]

            for i, task in enumerate(all_tasks):
                try:
                    output = str(task.output) if hasattr(task, 'output') and task.output else "No output"
                    task_outputs.append({
                        "task_number": i + 1,
                        "task_label": task_labels[i],
                        "agent": task.agent.role if hasattr(task, 'agent') else "Unknown",
                        "output": output[:2000]  # Limit to first 2000 chars
                    })
                except Exception as e:
                    logger.error(f"Error capturing task {i+1} output: {e}")
                    task_outputs.append({
                        "task_number": i + 1,
                        "task_label": task_labels[i],
                        "error": str(e)
                    })

            # Parse and store result
            logger.info(f"Crew completed. Result type: {type(result)}")

            if isinstance(result, str):
                try:
                    decision = json.loads(result)
                except json.JSONDecodeError:
                    decision = {"decision": "ERROR", "raw_output": result}
            else:
                decision = result if isinstance(result, dict) else {"decision": "UNKNOWN", "result": str(result)}

            self.sessions[session_id]["status"] = "completed"
            self.sessions[session_id]["result"] = decision
            self.sessions[session_id]["task_outputs"] = task_outputs  # Store individual task outputs
            self.sessions[session_id]["completed_at"] = datetime.now().isoformat()

            # Broadcast final decision via SSE
            await sse_manager.send_decision(session_id, decision)
            await sse_manager.send_phase_change(session_id, "completed")

            # Cleanup task tracking state
            if session_id in self.task_to_agent_map:
                del self.task_to_agent_map[session_id]
            if session_id in self.current_task_index:
                del self.current_task_index[session_id]
            logger.info(f"[CLEANUP] Removed task tracking for completed session {session_id}")

            logger.info(f"Analysis completed: {decision.get('decision', 'UNKNOWN')}")

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            self.sessions[session_id]["status"] = "failed"
            self.sessions[session_id]["error"] = str(e)
            self.sessions[session_id]["failed_at"] = datetime.now().isoformat()

            # Cleanup task tracking state
            if session_id in self.task_to_agent_map:
                del self.task_to_agent_map[session_id]
            if session_id in self.current_task_index:
                del self.current_task_index[session_id]
            logger.info(f"[CLEANUP] Removed task tracking for failed session {session_id}")

            # Broadcast error via SSE
            try:
                await sse_manager.send_error(
                    session_id,
                    f"Analysis failed: {str(e)}",
                    "ANALYSIS_ERROR"
                )
                await sse_manager.send_phase_change(session_id, "failed")
            except Exception as sse_error:
                logger.error(f"Failed to broadcast error via SSE: {sse_error}")

    async def _step_callback(self, session_id: str, step_output):
        """
        Callback for each agent step during CrewAI execution
        Broadcasts real-time updates to frontend via SSE

        Args:
            session_id: Session ID for this analysis
            step_output: Step output from CrewAI (contains agent and message info)
        """
        try:
            # Look up current agent from task-to-agent mapping
            task_index = self.current_task_index.get(session_id, 0)
            task_map = self.task_to_agent_map.get(session_id, [])
            agent_name = task_map[task_index] if task_index < len(task_map) else "unknown"

            output_type = type(step_output).__name__

            logger.info(f"[STEP CALLBACK] Type: {output_type}, Task: {task_index+1}/17, Agent: {agent_name}")

            # Extract and filter messages for curated UX (medium detail)
            message = None
            message_type = "step"

            if output_type == 'AgentFinish':
                # ✅ SHOW: Final conclusions (user wants to see this)
                if hasattr(step_output, 'output'):
                    output_text = str(step_output.output)
                    # Only show substantial conclusions (not empty/error messages)
                    if len(output_text) > 100:
                        message = f"✅ {output_text[:800]}"  # Longer for conclusions
                        message_type = "conclusion"
                        logger.info(f"[STEP CALLBACK] Broadcasting conclusion ({len(output_text)} chars)")

            elif hasattr(step_output, 'thought') and step_output.thought:
                # ✅ SHOW: Agent reasoning (user wants to see thoughts)
                thought_text = str(step_output.thought)
                # Filter out noisy/repetitive thoughts
                if len(thought_text) > 20 and not thought_text.startswith("I tried reusing"):
                    message = f"💭 {thought_text[:500]}"
                    message_type = "thought"
                    logger.info(f"[STEP CALLBACK] Broadcasting thought ({len(thought_text)} chars)")

            # ❌ SKIP: Tool results (too noisy for medium detail)
            # ❌ SKIP: Other step types (TaskOutput, dict, etc.)
            # Only show meaningful thoughts and conclusions

            # Broadcast to frontend via SSE if we have a message
            if message and len(message.strip()) > 0:
                await sse_manager.send_agent_message(
                    session_id,
                    agent_name,
                    message,
                    message_type  # Use dynamic message_type (thought/conclusion/step)
                )
                logger.info(f"[STEP CALLBACK] ✅ Broadcasted {message_type} to frontend")

                # Track task progression: AgentFinish with conclusion = task completed
                if output_type == 'AgentFinish' and message_type == "conclusion":
                    current_index = self.current_task_index.get(session_id, 0)
                    if current_index < 16:  # Don't increment beyond task 17 (index 16)
                        self.current_task_index[session_id] = current_index + 1
                        logger.info(f"[TASK PROGRESSION] Task {current_index+1} completed. Moving to task {current_index+2}/17")
            else:
                # Silently skip - this is expected for tool results and other filtered steps
                pass

        except Exception as e:
            logger.error(f"❌ Step callback error: {str(e)}", exc_info=True)

    async def get_result(self, session_id: str) -> Optional[dict]:
        """
        Get analysis result by session ID

        Args:
            session_id: Session ID to retrieve

        Returns:
            dict with session data, or None if not found
        """
        session = self.sessions.get(session_id)
        if not session:
            logger.warning(f"Session not found: {session_id}")
            return None

        return {
            "session_id": session_id,
            "status": session["status"],
            "company_data": session["company_data"],
            "result": session.get("result"),
            "task_outputs": session.get("task_outputs", []),  # Individual task outputs
            "error": session.get("error"),
            "message": session.get("message"),
            "completed_at": session.get("completed_at"),
            "failed_at": session.get("failed_at")
        }

    def get_session_count(self) -> int:
        """Get count of active sessions"""
        return len(self.sessions)

    def clear_session(self, session_id: str) -> bool:
        """
        Clear a specific session

        Args:
            session_id: Session ID to clear

        Returns:
            True if session was found and cleared, False otherwise
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleared session: {session_id}")
            return True
        return False


# Global orchestrator instance
orchestrator = VCCouncilOrchestrator()
