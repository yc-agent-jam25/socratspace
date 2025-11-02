# VC Council - System Architecture

**Last Updated:** November 2, 2025
**Version:** 2.0 (17-Task Sequential Architecture)

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Design Philosophy](#design-philosophy)
3. [Architecture Diagrams](#architecture-diagrams)
4. [Component Deep Dive](#component-deep-dive)
5. [Data Flow](#data-flow)
6. [Why This Architecture?](#why-this-architecture)
7. [Comparison to Alternatives](#comparison-to-alternatives)

---

## System Overview

### What is VC Council?

VC Council is an **8-agent AI investment committee** that evaluates startup investment opportunities through structured, adversarial debate. It simulates a real venture capital partnership meeting where specialists present research, advocates debate both sides, and a lead partner makes the final decision.

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  (React + TypeScript + Material-UI + WebSocket Client)      │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP REST API + WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Crew Orchestrator                         │ │
│  │  (Manages 17 sequential tasks across 5 rounds)        │ │
│  └──────────────────┬─────────────────────────────────────┘ │
│                     │                                        │
│  ┌──────────────────▼─────────────────────────────────────┐ │
│  │                 CrewAI Framework                        │ │
│  │  (Coordinates 8 agents through 17 tasks sequentially) │ │
│  └──────────────────┬─────────────────────────────────────┘ │
│                     │                                        │
│  ┌──────────────────▼─────────────────────────────────────┐ │
│  │              8 AI Agents (GPT-4 / Claude)              │ │
│  │  - Market Researcher    - Bull Advocate                │ │
│  │  - Founder Evaluator    - Bear Advocate                │ │
│  │  - Product Critic       - Risk Assessor                │ │
│  │  - Financial Analyst    - Lead Partner                 │ │
│  └──────────────────┬─────────────────────────────────────┘ │
│                     │                                        │
│  ┌──────────────────▼─────────────────────────────────────┐ │
│  │              MCP Tools (via Metorial SDK)              │ │
│  │  - Apify Web Scraper    - GitHub Analyzer              │ │
│  │  - HackerNews Search    - Exa Search                   │ │
│  └──────────────────┬─────────────────────────────────────┘ │
└────────────────────┬│──────────────────────────────────────┘
                     ││
┌────────────────────▼▼──────────────────────────────────────┐
│              Metorial MCP Platform                          │
│  (Deploys and runs MCP servers in cloud)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Design Philosophy

### 1. **Sequential Tasks = Real VC Meeting**

**Design Decision:** Use 17 sequential tasks instead of parallel research + sequential debate.

**Reasoning:**
- Real VC partner meetings don't have "research phase then debate phase"
- Partners discuss topics one at a time: market, then team, then product, then financials
- Each topic has focused discussion before moving to next
- This matches how humans actually make investment decisions

**Example:**
```
Real VC Meeting:
├─ Topic 1: "Let's discuss the market"
│  ├─ Market expert presents findings
│  ├─ Optimist argues opportunity is huge
│  ├─ Skeptic points out competition
│  └─ Risk person flags market timing concerns
├─ Topic 2: "Now let's discuss the team"
│  ├─ People expert presents founder evaluation
│  ├─ Optimist highlights founder strengths
│  └─ Skeptic points out experience gaps
└─ ...
```

Our 17-task architecture mirrors this exactly.

---

### 2. **Independent Round Contexts = Focused Discussions**

**Design Decision:** Each topic round (1-4) has independent context. Only final decision (round 5) sees everything.

**Reasoning:**

**Problem with "full context everywhere":**
```
If every task sees all previous tasks:
- Market discussion agent sees financial discussion (irrelevant)
- Token costs explode (16 tasks × context = massive)
- Agents get distracted by unrelated topics
- Slower execution (more tokens to process)
```

**Solution with independent contexts:**
```
Round 1 (Market):
  Task 1 (Market Researcher): context = []
  Task 2 (Bull): context = [Task 1]
  Task 3 (Bear): context = [Task 1, Task 2]
  Task 4 (Risk): context = [Task 1, Task 2, Task 3]
  ↓ Market discussion is self-contained

Round 2 (Team):
  Task 5 (Founder Evaluator): context = []  ← Fresh start!
  Task 6 (Bull): context = [Task 5]
  Task 7 (Bear): context = [Task 5, Task 6]
  Task 8 (Risk): context = [Task 5, Task 6, Task 7]
  ↓ Team discussion is self-contained

Round 5 (Decision):
  Task 17 (Lead Partner): context = [Tasks 1-16]  ← Sees EVERYTHING
```

**Benefits:**
- ✅ **Faster**: Less context per task = fewer tokens to process
- ✅ **Cheaper**: ~70% token cost reduction vs full context
- ✅ **More focused**: Agents stay on topic
- ✅ **Better quality**: Each discussion is deep, not distracted

**Why this works:**
- Market experts don't need financial data to assess TAM
- Team evaluators don't need product details to check GitHub
- Lead Partner synthesizes everything at the end

---

### 3. **All Agents Get Tools = Evidence-Based Debate**

**Design Decision:** Bull and Bear agents have access to all MCP tools, not just research agents.

**Reasoning:**

**Old approach (tools only for researchers):**
```
❌ Research Phase:
  - Market Researcher scrapes competitors → writes memo
  - Founder Evaluator checks GitHub → writes memo

❌ Debate Phase:
  - Bull reads memos, argues without new data
  - Bear reads memos, argues without new data

Problem: Bull/Bear are just "memo readers" with no ability to verify claims
```

**New approach (tools for everyone):**
```
✅ Round 1: Market Discussion
  - Market Researcher: Scrapes 3 competitor sites
  - Bull: "This market is huge!" → Calls Exa to find supporting trend data
  - Bear: "Really? Let me check..." → Calls HackerNews to find skepticism
  - Risk: Reviews both sides' evidence

Result: Evidence-based debate, not opinion-based
```

**Tool Assignment Strategy:**
```python
# Specialist agents - tools for their domain
market_researcher = Agent(
    tools=[ApifyScraperTool(), HackerNewsSearchTool(), ExaSearchTool()]
)

founder_evaluator = Agent(
    tools=[GitHubAnalyzerTool(), ExaSearchTool()]
)

# Debate agents - ALL tools (need evidence for arguments)
bull_agent = Agent(
    tools=[ApifyScraperTool(), HackerNewsSearchTool(),
           GitHubAnalyzerTool(), ExaSearchTool()]
)

bear_agent = Agent(
    tools=[ApifyScraperTool(), HackerNewsSearchTool(),
           GitHubAnalyzerTool(), ExaSearchTool()]
)

# Decision agent - NO tools (just reviews conversation)
lead_partner = Agent(
    tools=[]  # Synthesizes, doesn't research
)
```

**Why Bull/Bear need tools:**
1. **Verification**: Can fact-check specialist claims
2. **New evidence**: Can find data specialists missed
3. **Counter-arguments**: Can gather opposing evidence mid-debate
4. **Realistic**: Real VCs don't just read memos, they do their own digging

---

### 4. **CrewAI Sequential Process = Automatic Turn-Taking**

**Design Decision:** Use `Process.sequential` with context parameter for conversation flow.

**Reasoning:**

CrewAI's sequential process ensures:
1. **Tasks execute in order** (Task 1, then 2, then 3, etc.)
2. **Context parameter** makes previous task outputs available
3. **No manual orchestration** needed for turn-taking
4. **Agents speak when it's their turn** automatically

**How it works:**
```python
# Task 1: Market Researcher speaks first
task_1 = Task(
    description="Research the market...",
    agent=market_researcher,
    context=[]  # No previous context
)

# Task 2: Bull speaks second, sees Task 1
task_2 = Task(
    description="Argue bull case for market...",
    agent=bull_agent,
    context=[task_1]  # Sees market research
)

# Task 3: Bear speaks third, sees Tasks 1-2
task_3 = Task(
    description="Argue bear case...",
    agent=bear_agent,
    context=[task_1, task_2]  # Sees research + bull case
)

# CrewAI executes these in order automatically
crew = Crew(
    agents=[market_researcher, bull_agent, bear_agent],
    tasks=[task_1, task_2, task_3],
    process=Process.sequential  # ← This ensures order
)
```

**Alternative approaches we rejected:**
- ❌ **Custom turn-taking logic**: Complex, error-prone
- ❌ **Parallel execution**: Can't respond to each other
- ❌ **Group chat**: No control over speaking order

**Why sequential works:**
- ✅ Simple and reliable
- ✅ Guaranteed conversation order
- ✅ Context automatically passed between tasks
- ✅ CrewAI handles all orchestration

---

## Architecture Diagrams

### 1. High-Level System Flow

```
┌─────────────┐
│   User      │
│ (Frontend)  │
└──────┬──────┘
       │ POST /api/analyze
       │ {company_name, website, ...}
       ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│                                         │
│  ┌────────────────────────────────┐   │
│  │  VCCouncilOrchestrator         │   │
│  │  - Creates session_id          │   │
│  │  - Builds 17 tasks             │   │
│  │  - Launches CrewAI crew        │   │
│  └────────────┬───────────────────┘   │
│               │                        │
│  ┌────────────▼───────────────────┐   │
│  │  CrewAI Crew                   │   │
│  │  - Executes 17 tasks in order  │   │
│  │  - Manages agent interactions  │   │
│  │  - Calls tools as needed       │   │
│  └────────────┬───────────────────┘   │
│               │                        │
│  ┌────────────▼───────────────────┐   │
│  │  8 AI Agents (GPT-4/Claude)    │   │
│  │  - Process task instructions   │   │
│  │  - Invoke MCP tools            │   │
│  │  - Generate outputs            │   │
│  └────────────┬───────────────────┘   │
└───────────────┼────────────────────────┘
                │
                │ Tool calls via Metorial SDK
                ▼
┌─────────────────────────────────────────┐
│       Metorial MCP Platform             │
│  ┌─────────────────────────────────┐   │
│  │  Deployed MCP Servers           │   │
│  │  - Apify Web Scraper            │   │
│  │  - GitHub Analyzer              │   │
│  │  - HackerNews Search            │   │
│  │  - Exa Search Engine            │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                │
                │ Results
                ▼
        (Back to agents)
```

---

### 2. The 17-Task Sequential Flow

```
ROUND 1: MARKET DISCUSSION (Independent context)
┌──────────────────────────────────────────────────────────┐
│ Task 1: Market Researcher                                │
│   - context: []                                          │
│   - Tools: Apify, HackerNews, Exa                        │
│   - Output: Market analysis (TAM, growth, competitors)   │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 2: Bull Agent                                       │
│   - context: [Task 1]                                    │
│   - Tools: ALL tools (can verify/add evidence)           │
│   - Output: Bull case for market opportunity             │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 3: Bear Agent                                       │
│   - context: [Task 1, Task 2]                            │
│   - Tools: ALL tools (can counter Bull's claims)         │
│   - Output: Bear case + rebuttals to Bull                │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 4: Risk Assessor                                    │
│   - context: [Task 1, Task 2, Task 3]                    │
│   - Tools: Apify, HackerNews (find risks)                │
│   - Output: Market risk assessment                       │
└──────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════

ROUND 2: TEAM DISCUSSION (Independent context - FRESH START)
┌──────────────────────────────────────────────────────────┐
│ Task 5: Founder Evaluator                                │
│   - context: []  ← FRESH START (no Round 1)              │
│   - Tools: GitHub, Exa                                   │
│   - Output: Founder evaluation                           │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 6: Bull Agent                                       │
│   - context: [Task 5]                                    │
│   - Output: Bull case for team                           │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 7: Bear Agent                                       │
│   - context: [Task 5, Task 6]                            │
│   - Output: Bear case for team concerns                  │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 8: Risk Assessor                                    │
│   - context: [Task 5, Task 6, Task 7]                    │
│   - Output: Execution risk assessment                    │
└──────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════

ROUND 3: PRODUCT DISCUSSION (Independent context - FRESH START)
┌──────────────────────────────────────────────────────────┐
│ Task 9: Product Critic                                   │
│   - context: []  ← FRESH START (no previous rounds)      │
│   - Tools: Apify, Exa                                    │
│   - Output: Product + moat analysis                      │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 10: Bull Agent                                      │
│   - context: [Task 9]                                    │
│   - Output: Bull case for product                        │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 11: Bear Agent                                      │
│   - context: [Task 9, Task 10]                           │
│   - Output: Bear case for product weaknesses             │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 12: Market Researcher                               │
│   - context: [Task 9, Task 10, Task 11]                  │
│   - Output: Product-market fit assessment                │
└──────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════

ROUND 4: FINANCIAL DISCUSSION (Independent context - FRESH START)
┌──────────────────────────────────────────────────────────┐
│ Task 13: Financial Analyst                               │
│   - context: []  ← FRESH START (no previous rounds)      │
│   - Tools: None (works with provided data)               │
│   - Output: Financial analysis (LTV:CAC, burn, runway)   │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 14: Bull Agent                                      │
│   - context: [Task 13]                                   │
│   - Output: Bull case for financials                     │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 15: Bear Agent                                      │
│   - context: [Task 13, Task 14]                          │
│   - Output: Bear case for financial risks                │
└────────────────┬─────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────┐
│ Task 16: Risk Assessor                                   │
│   - context: [Task 13, Task 14, Task 15]                 │
│   - Output: Financial risk assessment                    │
└──────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════

ROUND 5: FINAL DECISION (Sees EVERYTHING)
┌──────────────────────────────────────────────────────────┐
│ Task 17: Lead Partner                                    │
│   - context: [Tasks 1-16]  ← FULL DEBATE HISTORY         │
│   - Tools: None (synthesizes only)                       │
│   - Output: PASS/MAYBE/INVEST decision + memo            │
└──────────────────────────────────────────────────────────┘
```

**Key Insight:** Notice how each round starts fresh (context=[]) except the final decision which sees everything. This creates focused topic discussions while ensuring the decision-maker has the full picture.

---

### 3. Context Flow Visualization

```
Round 1: Market
┌─────────┐
│ Task 1  │ (no context)
└────┬────┘
     │
     ├──► Task 2 (sees Task 1)
     │
     ├──► Task 3 (sees Tasks 1-2)
     │
     └──► Task 4 (sees Tasks 1-3)

Round 2: Team
┌─────────┐
│ Task 5  │ (no context - FRESH START)
└────┬────┘
     │
     ├──► Task 6 (sees Task 5)
     │
     ├──► Task 7 (sees Tasks 5-6)
     │
     └──► Task 8 (sees Tasks 5-7)

Round 3: Product
┌─────────┐
│ Task 9  │ (no context - FRESH START)
└────┬────┘
     │
     ├──► Task 10 (sees Task 9)
     │
     ├──► Task 11 (sees Tasks 9-10)
     │
     └──► Task 12 (sees Tasks 9-11)

Round 4: Financial
┌─────────┐
│ Task 13 │ (no context - FRESH START)
└────┬────┘
     │
     ├──► Task 14 (sees Task 13)
     │
     ├──► Task 15 (sees Tasks 13-14)
     │
     └──► Task 16 (sees Tasks 13-15)

Round 5: Decision
┌─────────┐
│ Task 17 │ (sees Tasks 1-16 - EVERYTHING)
└─────────┘
```

**Token Efficiency:**
- Without independent contexts: Each task would see ALL previous tasks → massive context
- With independent contexts: Each round is self-contained → minimal context
- Decision task: Only one that needs full context, and it gets it

---

## Component Deep Dive

### Backend Components

#### 1. FastAPI Application (`main.py`)

**Purpose:** HTTP server and WebSocket gateway

**Responsibilities:**
- Serve REST API endpoints
- Manage WebSocket connections for real-time updates
- Handle CORS for frontend communication
- Route requests to orchestrator

**Key Endpoints:**
```python
POST /api/analyze
  ├─ Input: {company_name, website, founder_github, ...}
  ├─ Creates session_id
  ├─ Starts analysis in background
  └─ Returns: {status: "started", session_id: "..."}

GET /api/analysis/{session_id}
  ├─ Input: session_id
  └─ Returns: {status, result, error}

WebSocket /ws
  ├─ Real-time event stream
  └─ Events: phase_change, agent_message, decision, error
```

---

#### 2. Crew Orchestrator (`services/crew_orchestrator.py`)

**Purpose:** Coordinates the entire 17-task debate flow

**Architecture:**
```python
class VCCouncilOrchestrator:
    def __init__(self):
        self.sessions = {}  # Track active analyses

    async def start_analysis(self, company_data: dict) -> str:
        """
        Entry point for new analysis

        1. Create session_id
        2. Store session in self.sessions
        3. Launch _run_analysis() in background
        4. Return session_id immediately
        """

    async def _run_analysis(self, session_id: str, company_data: dict):
        """
        Execute 17 tasks through CrewAI

        Phase 1: Create all 8 agents
        Phase 2: Create all 17 tasks with correct context
        Phase 3: Build CrewAI Crew with sequential process
        Phase 4: Execute crew.kickoff()
        Phase 5: Parse result and broadcast
        """

    async def get_result(self, session_id: str) -> dict:
        """Poll for analysis result"""
```

**Why background execution?**
- Analysis takes 3-5 minutes
- Can't block HTTP request that long
- Return session_id immediately, user polls for updates
- WebSocket provides real-time progress

**Why session management?**
- Multiple users can run analyses simultaneously
- Each gets unique session_id
- Results stored in memory (could be Redis in production)

---

#### 3. Agent Definitions (`agents/definitions.py`)

**Purpose:** Create 8 distinct AI agents with tools and personalities

**Agent Roles:**

```python
1. Market Researcher
   ├─ Role: Research market size, growth, competition
   ├─ Tools: Apify, HackerNews, Exa
   ├─ Delegation: No (focus on own research)
   └─ Used in: Tasks 1, 12

2. Founder Evaluator
   ├─ Role: Assess team quality and execution ability
   ├─ Tools: GitHub, Exa
   ├─ Delegation: No
   └─ Used in: Task 5

3. Product Critic
   ├─ Role: Evaluate product moat and defensibility
   ├─ Tools: Apify, Exa
   ├─ Delegation: No
   └─ Used in: Task 9

4. Financial Analyst
   ├─ Role: Calculate LTV:CAC, burn, runway
   ├─ Tools: None (works with provided data)
   ├─ Delegation: No
   └─ Used in: Task 13

5. Risk Assessor
   ├─ Role: Identify catastrophic failure modes
   ├─ Tools: Apify, HackerNews
   ├─ Delegation: No
   └─ Used in: Tasks 4, 8, 16

6. Bull Agent
   ├─ Role: Build strongest case FOR investing
   ├─ Tools: ALL tools (needs evidence)
   ├─ Delegation: Yes (can ask specialists for more data)
   └─ Used in: Tasks 2, 6, 10, 14

7. Bear Agent
   ├─ Role: Build strongest case AGAINST investing
   ├─ Tools: ALL tools (needs counter-evidence)
   ├─ Delegation: Yes
   └─ Used in: Tasks 3, 7, 11, 15

8. Lead Partner
   ├─ Role: Make final PASS/MAYBE/INVEST decision
   ├─ Tools: None (synthesizes only)
   ├─ Delegation: No
   └─ Used in: Task 17
```

**Why these 8 specific agents?**

1. **Specialist agents (5)**: Each focuses on one domain
   - Market Researcher → market knowledge
   - Founder Evaluator → people assessment
   - Product Critic → product analysis
   - Financial Analyst → numbers
   - Risk Assessor → failure modes

2. **Debate agents (2)**: Adversarial perspectives
   - Bull → optimistic case (find reasons to invest)
   - Bear → pessimistic case (find reasons to pass)
   - Creates intellectual honesty through debate

3. **Decision agent (1)**: Final authority
   - Lead Partner → synthesizes all perspectives
   - Makes decisive call with full context

**Why give Bull/Bear ALL tools?**
- They need to verify specialist claims
- Can gather new evidence mid-debate
- Prevents "memo reader" problem
- Creates dynamic, evidence-based arguments

---

#### 4. Task Definitions (`tasks/debate_tasks.py`)

**Purpose:** Define what each of the 17 tasks should accomplish

**Task Structure:**
```python
def create_market_researcher_task(
    agents: dict,
    company_data: dict,
    context: List[Task] = []
) -> Task:
    return Task(
        description="""
        Clear instructions for the agent:
        - What to research
        - Which tools to use
        - What format to output
        """,
        expected_output="Specific output format",
        agent=agents["market_researcher"],
        context=context  # Previous tasks this agent can see
    )
```

**Why separate task creation functions?**
- **Reusability**: Same agent used in multiple tasks (Bull in 4 tasks)
- **Clarity**: Each function clearly defines one step
- **Context control**: Explicit context parameter shows dependencies
- **Testability**: Can test individual tasks in isolation

**Task Naming Convention:**
```
create_<agent>_<topic>_task()

Examples:
- create_bull_market_task() → Bull argues market (Task 2)
- create_bear_team_task() → Bear argues team (Task 7)
- create_risk_financial_task() → Risk assesses financials (Task 16)
```

---

#### 5. MCP Tools (`tools/*.py`)

**Purpose:** CrewAI-compatible wrappers for Metorial MCP servers

**Tool Architecture:**
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from tools.mcp_client import mcp_client
import asyncio

class ApifyScraperInput(BaseModel):
    """Pydantic model for input validation"""
    url: str = Field(..., description="Website to scrape")
    extract_type: str = Field(default="all", description="What to extract")

class ApifyScraperTool(BaseTool):
    """CrewAI tool that wraps Metorial MCP call"""

    name: str = "Web Scraper"
    description: str = "Scrapes websites for competitor data..."
    args_schema: Type[BaseModel] = ApifyScraperInput

    def _run(self, url: str, extract_type: str = "all") -> str:
        """
        CrewAI calls this method when agent invokes tool

        Flow:
        1. Agent decides to use tool
        2. CrewAI validates inputs via args_schema
        3. CrewAI calls _run() with validated params
        4. We call mcp_client.call_mcp()
        5. Return formatted result to agent
        """
        async def scrape():
            result = await mcp_client.call_mcp(
                mcp_name="apify",
                tool_name="scrape_website",
                parameters={"url": url, "extractType": extract_type}
            )
            return format_result(result)

        return asyncio.run(scrape())
```

**Why this architecture?**
1. **CrewAI integration**: Extends BaseTool for automatic discovery
2. **Input validation**: Pydantic models prevent bad inputs
3. **Type safety**: args_schema provides IDE autocomplete
4. **Error handling**: Can catch and format MCP errors gracefully

**Tool Execution Flow:**
```
Agent thinking → "I need competitor data"
     ↓
Agent invokes: ApifyScraperTool(url="competitor.com")
     ↓
CrewAI validates input via ApifyScraperInput schema
     ↓
CrewAI calls tool._run(url="competitor.com", extract_type="all")
     ↓
Tool calls mcp_client.call_mcp("apify", "scrape_website", {...})
     ↓
MCP Client calls Metorial SDK: metorial.run(...)
     ↓
Metorial executes deployed Apify MCP server
     ↓
Result flows back: MCP → SDK → Client → Tool → Agent
     ↓
Agent receives: "Scraped competitor.com: [data here]"
     ↓
Agent incorporates result into response
```

---

#### 6. MCP Client (`tools/mcp_client.py`)

**Purpose:** Unified interface to Metorial MCP platform

**Why Metorial SDK approach?**

**Alternative 1 (Raw HTTP):**
```python
# ❌ Complex manual implementation
response = requests.post(
    "https://api.metorial.com/v1/mcp/invoke",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "deployment_id": "svd_...",
        "tool_name": "scrape_website",
        "parameters": {"url": "..."}
    }
)
# Then manually parse response, handle errors, etc.
```

**Alternative 2 (Metorial SDK with .run()):**
```python
# ✅ Simple, uses LLM to invoke tools
from metorial import Metorial

metorial = Metorial(api_key=api_key)
result = await metorial.run(
    message="Scrape website competitor.com",
    server_deployments=["svd_apify_..."],
    client=openai_client,
    model="gpt-4o"
)
# SDK handles everything: parsing message, calling tool, formatting result
```

**We chose Alternative 2 because:**
- ✅ **Simpler code**: No manual HTTP calls
- ✅ **LLM handles tool selection**: We just describe what we want
- ✅ **Better error handling**: SDK handles retries and failures
- ✅ **Cost is negligible**: ~$0.0001 per call for the parsing LLM
- ✅ **Works perfectly with CrewAI**: Returns structured RunResult

**Trade-off:**
- 🔵 Adds small latency (LLM parses message → selects tool → invokes)
- 🟢 But saves massive development time
- 🟢 And we'd use LLM anyway for parsing complex results

---

## Data Flow

### 1. User Submits Analysis Request

```
┌──────────┐
│ Frontend │
└─────┬────┘
      │ POST /api/analyze
      │ {
      │   "company_name": "Acme AI",
      │   "website": "https://acme.ai",
      │   "founder_github": "founder123",
      │   "industry": "AI/ML",
      │   "product_description": "AI-powered analytics",
      │   "financial_metrics": {
      │     "monthly_revenue": 50000,
      │     "monthly_burn": 30000
      │   }
      │ }
      ▼
┌─────────────────┐
│ FastAPI Router  │
│ (api/routes.py) │
└─────┬───────────┘
      │
      ▼
┌──────────────────────────────────┐
│ VCCouncilOrchestrator            │
│ orchestrator.start_analysis(data)│
└─────┬────────────────────────────┘
      │
      │ 1. Generate session_id = uuid4()
      │ 2. Store in sessions dict
      │ 3. Launch background task
      │
      ▼
┌──────────────────────────────────┐
│ Return immediately               │
│ {                                │
│   status: "started",             │
│   session_id: "abc-123...",      │
│   message: "Analysis started"    │
│ }                                │
└──────────────────────────────────┘
```

---

### 2. Background Analysis Execution

```
Background Task: orchestrator._run_analysis()

Step 1: Create all 8 agents
┌────────────────────────────────┐
│ agents = create_all_agents()   │
│ {                              │
│   "market_researcher": Agent,  │
│   "founder_evaluator": Agent,  │
│   "product_critic": Agent,     │
│   "financial_analyst": Agent,  │
│   "risk_assessor": Agent,      │
│   "bull_agent": Agent,         │
│   "bear_agent": Agent,         │
│   "lead_partner": Agent        │
│ }                              │
└────────────────────────────────┘

Step 2: Create Round 1 tasks (Market)
┌────────────────────────────────────────┐
│ task_1 = create_market_researcher_task(│
│     agents=agents,                     │
│     company_data=company_data,         │
│     context=[]  # First task           │
│ )                                      │
│                                        │
│ task_2 = create_bull_market_task(      │
│     agents=agents,                     │
│     company_data=company_data,         │
│     context=[task_1]  # Sees Task 1    │
│ )                                      │
│                                        │
│ task_3 = create_bear_market_task(...)  │
│ task_4 = create_risk_market_task(...)  │
└────────────────────────────────────────┘

Step 3: Create Round 2 tasks (Team)
┌────────────────────────────────────────┐
│ task_5 = create_founder_evaluator_task(│
│     agents=agents,                     │
│     company_data=company_data,         │
│     context=[]  # FRESH START          │
│ )                                      │
│                                        │
│ task_6 = create_bull_team_task(...)    │
│ task_7 = create_bear_team_task(...)    │
│ task_8 = create_risk_team_task(...)    │
└────────────────────────────────────────┘

Step 4: Create Round 3 tasks (Product)
┌────────────────────────────────────────┐
│ task_9 = create_product_critic_task(   │
│     context=[]  # FRESH START          │
│ )                                      │
│ task_10 = create_bull_product_task(...)│
│ task_11 = create_bear_product_task(...)│
│ task_12 = create_market_product_task(.)│
└────────────────────────────────────────┘

Step 5: Create Round 4 tasks (Financial)
┌────────────────────────────────────────┐
│ task_13 = create_financial_analyst_task│
│     context=[]  # FRESH START          │
│ )                                      │
│ task_14 = create_bull_financial_task(..)│
│ task_15 = create_bear_financial_task(..)│
│ task_16 = create_risk_financial_task(..)│
└────────────────────────────────────────┘

Step 6: Create Round 5 task (Decision)
┌────────────────────────────────────────┐
│ task_17 = create_lead_partner_task(    │
│     agents=agents,                     │
│     company_data=company_data,         │
│     context=[                          │
│         task_1, task_2, ..., task_16   │
│     ]  # SEES ALL 16 TASKS             │
│ )                                      │
└────────────────────────────────────────┘

Step 7: Build CrewAI Crew
┌────────────────────────────────────────┐
│ crew = Crew(                           │
│     agents=list(agents.values()),      │
│     tasks=[                            │
│         task_1, task_2, ..., task_17   │
│     ],                                 │
│     process=Process.sequential,        │
│     verbose=True,                      │
│     step_callback=_step_callback       │
│ )                                      │
└────────────────────────────────────────┘

Step 8: Execute Crew
┌────────────────────────────────────────┐
│ result = await crew.kickoff(           │
│     inputs=company_data                │
│ )                                      │
│                                        │
│ CrewAI executes tasks 1-17 in order    │
│ Each task:                             │
│   - Gets context from previous tasks   │
│   - Agent processes with LLM           │
│   - Can invoke tools                   │
│   - Returns output                     │
│   - Output becomes available to next   │
└────────────────────────────────────────┘

Step 9: Parse and Store Result
┌────────────────────────────────────────┐
│ decision = json.loads(result)          │
│ {                                      │
│   "decision": "INVEST",                │
│   "reasoning": "...",                  │
│   "investment_memo": "...",            │
│   "calendar_events": [...]             │
│ }                                      │
│                                        │
│ sessions[session_id] = {               │
│   "status": "completed",               │
│   "result": decision                   │
│ }                                      │
└────────────────────────────────────────┘

Step 10: Broadcast Final Decision
┌────────────────────────────────────────┐
│ websocket_manager.send_decision(       │
│     decision                           │
│ )                                      │
│                                        │
│ → All connected WebSocket clients      │
│   receive decision                     │
└────────────────────────────────────────┘
```

---

### 3. Real-Time WebSocket Updates

```
Throughout execution, step_callback() broadcasts events:

Event 1: Phase Change
┌─────────────────────────────────────┐
│ WebSocket message:                  │
│ {                                   │
│   "type": "phase_change",           │
│   "data": {                         │
│     "phase": "market_discussion"    │
│   }                                 │
│ }                                   │
└─────────────────────────────────────┘

Event 2: Agent Message
┌─────────────────────────────────────┐
│ WebSocket message:                  │
│ {                                   │
│   "type": "agent_message",          │
│   "data": {                         │
│     "agent": "market_researcher",   │
│     "message": "Analyzing market...",│
│     "message_type": "step"          │
│   }                                 │
│ }                                   │
└─────────────────────────────────────┘

Event 3: Final Decision
┌─────────────────────────────────────┐
│ WebSocket message:                  │
│ {                                   │
│   "type": "decision",               │
│   "data": {                         │
│     "decision": "INVEST",           │
│     "reasoning": "...",             │
│     "investment_memo": "...",       │
│     "calendar_events": [...]        │
│   }                                 │
│ }                                   │
└─────────────────────────────────────┘
```

---

### 4. Tool Invocation Flow

```
Example: Task 2 (Bull argues market)

Agent receives task:
┌──────────────────────────────────────────┐
│ Task 2 context contains:                 │
│ - Task 1 output (market research)        │
│ - Company data                           │
│                                          │
│ Agent sees:                              │
│ "Market Researcher found $5B TAM with    │
│  40% growth. 3 competitors exist."       │
└──────────────────────────────────────────┘

Agent decides to gather more evidence:
┌──────────────────────────────────────────┐
│ Agent thinking:                          │
│ "I need more positive market signals     │
│  to strengthen bull case. Let me search  │
│  for market trend data."                 │
│                                          │
│ Agent invokes tool:                      │
│ ExaSearchTool(                           │
│   query="AI market growth trends 2025"   │
│ )                                        │
└──────────────────────────────────────────┘

Tool execution:
┌──────────────────────────────────────────┐
│ 1. CrewAI validates input via schema     │
│ 2. Calls ExaSearchTool._run(query="...") │
│ 3. Tool calls mcp_client.call_mcp(       │
│      mcp_name="exa",                     │
│      tool_name="search",                 │
│      parameters={"query": "..."}         │
│    )                                     │
│ 4. MCP Client calls Metorial SDK:        │
│    metorial.run(                         │
│      message="Search: AI market...",     │
│      server_deployments=["svd_exa_..."],│
│      client=openai_client,               │
│      model="gpt-4o"                      │
│    )                                     │
│ 5. Metorial executes Exa MCP server      │
│ 6. Result flows back through chain       │
└──────────────────────────────────────────┘

Agent receives tool result:
┌──────────────────────────────────────────┐
│ "Found 5 sources confirming AI market    │
│  growing 45% YoY. Institutional investors│
│  allocating $2B+ to AI tools in 2025."   │
└──────────────────────────────────────────┘

Agent incorporates into response:
┌──────────────────────────────────────────┐
│ Bull Case for Market:                    │
│                                          │
│ The AI market opportunity is MASSIVE.    │
│ Market Researcher found $5B TAM at 40%   │
│ growth. I verified with Exa search and   │
│ found 5 independent sources confirming   │
│ 45% YoY growth. Institutional investors  │
│ are pouring $2B+ into this space.        │
│                                          │
│ With only 3 competitors, there's room    │
│ for a strong #2 or #3 player...          │
└──────────────────────────────────────────┘

Task 2 output becomes available to Task 3 (Bear)
```

---

## Why This Architecture?

### Problem Statement

We needed to build an **AI investment committee** that:
1. Evaluates startups rigorously (not just hype)
2. Considers multiple perspectives (not single-agent bias)
3. Uses real data (not hallucinations)
4. Makes decisions quickly (< 5 minutes)
5. Explains reasoning (not black box)
6. Can be demonstrated live (hackathon requirement)

### Why NOT Alternative Architectures?

#### ❌ Alternative 1: Single LLM Call

```python
# Just ask GPT-4 directly
decision = openai.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": f"Should I invest in {company_name}?"
    }]
)
```

**Problems:**
- ❌ Single perspective (no debate)
- ❌ No real data (hallucinates facts)
- ❌ No structured reasoning
- ❌ Not reproducible
- ❌ Boring demo

---

#### ❌ Alternative 2: Parallel Research + Sequential Debate

```python
# Old architecture we considered

Phase 1: Parallel Research (5 agents simultaneously)
  - All 5 research agents run in parallel
  - Each produces memo

Phase 2: Sequential Debate
  - Bull reads all 5 memos → argues
  - Bear reads all 5 memos → argues

Phase 3: Decision
  - Lead Partner reads memos + debate → decides
```

**Why we rejected it:**

1. **Not how VCs actually work**
   - Real partners don't read 5 memos then debate
   - They discuss topics one at a time
   - Market discussion happens before product discussion

2. **No mid-debate research**
   - What if Bull wants to verify a claim during debate?
   - In this model, Bull can't call tools
   - Debate becomes "memo reading contest"

3. **Massive context at debate phase**
   - Bull sees 5 full memos (could be 5000+ tokens)
   - Bear sees 5 memos + Bull's case (6000+ tokens)
   - Expensive and slow

4. **Less engaging demo**
   - "Parallel research" looks like loading spinner
   - No visible conversation flow
   - Harder to follow for audience

---

#### ❌ Alternative 3: Group Chat (All Agents Talk Freely)

```python
# LangGraph style group chat

Agents in chat room: [Market, Founder, Product, Financial, Risk, Bull, Bear, Lead]

Let them talk freely:
  Market: "I found $5B TAM"
  Bull: "That's great!"
  Product: "Wait, what about the product?"
  Bear: "The market is crowded"
  [Chaos ensues]
```

**Why we rejected it:**

1. **No conversation structure**
   - Who speaks when?
   - How do you prevent interruptions?
   - How do you ensure all topics covered?

2. **Token explosion**
   - Every message goes to all agents
   - Context grows quadratically
   - Becomes unmanageable quickly

3. **Reproducibility issues**
   - Different order of speaking each time
   - Can't guarantee quality
   - Hard to debug

4. **Not how real VCs work**
   - Real meetings have agendas
   - Topics covered sequentially
   - Lead partner controls flow

---

### ✅ Why Our Architecture Wins

#### 1. Mirrors Real VC Meetings

```
Real VC Partner Meeting:
├─ Agenda item 1: Market
│  ├─ Market expert presents
│  ├─ Optimist argues opportunity
│  ├─ Skeptic argues risks
│  └─ Discussion until consensus
├─ Agenda item 2: Team
│  ├─ People expert presents
│  ├─ Optimist argues strengths
│  └─ Skeptic argues gaps
└─ ...

Our 17-Task Architecture:
├─ Round 1: Market (Tasks 1-4)
│  ├─ Task 1: Market expert presents
│  ├─ Task 2: Bull argues opportunity
│  ├─ Task 3: Bear argues risks
│  └─ Task 4: Risk assessment
├─ Round 2: Team (Tasks 5-8)
│  ├─ Task 5: People expert presents
│  ├─ Task 6: Bull argues strengths
│  └─ Task 7: Bear argues gaps
└─ ...

Perfect match!
```

---

#### 2. Evidence-Based Debate

```
Traditional approach:
  Researcher → writes memo with data
  Debaters → read memo, argue from memory
  Problem: Can't verify claims, can't dig deeper

Our approach:
  Researcher → presents findings
  Bull → "Let me verify..." → calls tool → "Confirmed!"
  Bear → "But what about..." → calls tool → "Found evidence against"
  Result: Dynamic, evidence-based debate
```

**Example:**
```
Task 1 (Market Researcher):
"I estimate $5B TAM based on industry reports"

Task 2 (Bull):
"Let me verify this is growing rapidly..."
→ Calls ExaSearchTool("AI market growth 2025")
→ Gets: "45% YoY growth confirmed by 5 sources"
"STRONG bull case - rapidly growing $5B market!"

Task 3 (Bear):
"But is it crowded? Let me check competitors..."
→ Calls ApifyScraperTool("competitor1.com/pricing")
→ Gets: "Competitor raised $100M, pricing at $50k/year"
"WEAK - well-funded competition, pricing pressure likely"

Task 4 (Risk):
"Both valid points. Main risk: market timing if sentiment shifts"
```

This creates **intellectual honesty** - both sides use real data.

---

#### 3. Token Efficiency

**Full context approach:**
```
Task 1: 500 tokens
Task 2: 500 + 500 = 1000 tokens (sees Task 1)
Task 3: 500 + 1000 = 1500 tokens (sees Tasks 1-2)
Task 4: 500 + 1500 = 2000 tokens (sees Tasks 1-3)
Task 5: 500 + 2000 = 2500 tokens (sees Tasks 1-4)
...
Task 17: 500 + 8000 = 8500 tokens (sees Tasks 1-16)

Total context tokens: ~68,000 tokens
Cost: ~$2.00 per analysis
```

**Independent context approach:**
```
Round 1:
  Task 1: 500 tokens
  Task 2: 500 + 500 = 1000 tokens
  Task 3: 500 + 1000 = 1500 tokens
  Task 4: 500 + 1500 = 2000 tokens
  Subtotal: 5000 tokens

Round 2:
  Task 5: 500 tokens (FRESH START)
  Task 6: 500 + 500 = 1000 tokens
  Task 7: 500 + 1000 = 1500 tokens
  Task 8: 500 + 1500 = 2000 tokens
  Subtotal: 5000 tokens

Round 3: 5000 tokens (same pattern)
Round 4: 5000 tokens (same pattern)
Round 5:
  Task 17: 500 + 8000 = 8500 tokens (sees all)

Total context tokens: ~28,500 tokens
Cost: ~$0.85 per analysis

Savings: 58% cheaper! 🎉
```

**Why this works:**
- Market discussion doesn't need financial context
- Team discussion doesn't need product context
- Each round stays focused on its topic
- Only decision needs full context

---

#### 4. Great Live Demo

```
What audience sees in real-time:

[Phase: Market Discussion]
  Market Researcher: "Analyzing market... found $5B TAM, 40% growth"
  Bull: "Huge opportunity! Let me verify growth rate..."
  Bull: "Confirmed 45% YoY growth via Exa search"
  Bear: "But market is crowded. Checking competitors..."
  Bear: "Found 3 well-funded competitors at $50k pricing"
  Risk: "Market timing risk is HIGH"

[Phase: Team Discussion]
  Founder Evaluator: "Checking GitHub... founder has 1200 commits"
  Bull: "Strong technical founder!"
  Bear: "But no business co-founder - who handles sales?"
  Risk: "Execution risk: MEDIUM-HIGH"

[Phase: Final Decision]
  Lead Partner: "After reviewing all discussions..."
  Lead Partner: "DECISION: PASS"
  Lead Partner: "RATIONALE: Crowded market, team lacks business expertise..."

Audience reaction: "Wow, they're actually debating!"
```

**vs parallel research approach:**
```
What audience sees:

[Loading spinner for 3 minutes]
"Research complete. Debate starting..."
[More loading]
"Decision: PASS"

Audience reaction: "...that's it?"
```

---

#### 5. Modularity and Testing

```python
# Can test individual components

# Test single task
task_1 = create_market_researcher_task(agents, company_data, context=[])
result_1 = task_1.execute()
assert "TAM" in result_1

# Test single round
tasks_round_1 = [task_1, task_2, task_3, task_4]
crew = Crew(agents=agents, tasks=tasks_round_1)
result = crew.kickoff()
# Verify market discussion works

# Test full flow
all_17_tasks = [...]
crew = Crew(agents=agents, tasks=all_17_tasks)
result = crew.kickoff()
# Integration test
```

**Why this matters:**
- Debug individual tasks easily
- Test rounds in isolation
- Faster iteration during development
- Clear error localization

---

## Comparison to Alternatives

### vs LangGraph

**LangGraph:**
```python
# Define nodes and edges
graph = StateGraph()
graph.add_node("research", research_agent)
graph.add_node("debate", debate_agent)
graph.add_edge("research", "debate")
graph.compile()
```

**Pros:**
- ✅ Very flexible
- ✅ Explicit control flow

**Cons:**
- ❌ Manual state management
- ❌ Complex for 17 sequential tasks
- ❌ More code to write and maintain
- ❌ Harder to debug

**Why we chose CrewAI:**
- Sequential process is built-in
- Context parameter handles state automatically
- Less boilerplate
- Better for hackathon timeline

---

### vs AutoGen

**AutoGen:**
```python
# Group chat
agents = [market, founder, product, ...]
groupchat = GroupChat(agents=agents)
manager = GroupChatManager(groupchat=groupchat)
```

**Pros:**
- ✅ Great for free-form conversation
- ✅ Strong group chat features

**Cons:**
- ❌ Hard to control speaking order
- ❌ No built-in topic structure
- ❌ Can get chaotic with 8 agents
- ❌ Harder to ensure all topics covered

**Why we chose CrewAI:**
- Need structured turn-taking
- 17 specific tasks in specific order
- Context control is critical
- Simpler mental model

---

### vs Custom Orchestrator

**Custom:**
```python
# Write everything from scratch
class CustomOrchestrator:
    def run_task_1(self):
        # Call LLM manually
        # Manage context manually
        # Handle errors manually

    def run_task_2(self):
        # Repeat 17 times
```

**Pros:**
- ✅ Total control
- ✅ No framework limitations

**Cons:**
- ❌ Weeks of development time
- ❌ Reinventing the wheel
- ❌ More bugs
- ❌ Harder to maintain

**Why we chose CrewAI:**
- Hackathon timeline (24 hours)
- Framework handles edge cases
- Community support
- Battle-tested patterns

---

## Summary

### Architecture Principles

1. **Sequential tasks** = Structured conversation flow
2. **Independent contexts** = Focused discussions + token efficiency
3. **Tools for all** = Evidence-based debate
4. **CrewAI framework** = Simple orchestration
5. **Real-time WebSocket** = Engaging live demo

### Key Insights

1. **Context is expensive** - Only pass what's needed
2. **Tools create debates** - Bull/Bear need evidence-gathering capability
3. **Sequential > parallel** - Mirrors real decision-making
4. **Framework > custom** - Faster development, fewer bugs
5. **Structure > chaos** - 17 ordered tasks > free-form chat

### Design Trade-offs

| Decision | Trade-off | Why Worth It |
|----------|-----------|--------------|
| 17 sequential tasks | More complex than 5 phases | Matches real VC meetings |
| Independent contexts | Lead Partner has large context | 70% cost savings on other tasks |
| Tools for Bull/Bear | More API calls | Creates real debates |
| CrewAI framework | Less flexibility | 10x faster development |
| WebSocket updates | Additional complexity | Better live demo |

---

## Appendix: Real-World Example

### Sample Debate Transcript

```
Company: Acme AI
Product: AI-powered investment analysis platform

═══════════════════════════════════════════════════════
ROUND 1: MARKET DISCUSSION
═══════════════════════════════════════════════════════

[Task 1: Market Researcher]
Analyzing market for Acme AI...

[Tool Call: ApifyScraperTool(url="acme.ai")]
Scraped website. Product: AI investment analysis for VCs.

[Tool Call: HackerNewsSearchTool(query="AI investment tools")]
Found 15 HN discussions. Sentiment: 60% positive, 40% skeptical.

[Tool Call: ApifyScraperTool(url="competitor1.com")]
Competitor: InvestAI - $50k/year pricing, raised $100M Series B.

[Tool Call: ApifyScraperTool(url="competitor2.com")]
Competitor: SmartVC - $30k/year, 200+ customers.

MARKET ANALYSIS:
- TAM: $5B (bottom-up: 10k VC firms × $50k avg spend)
- Growth: 40% YoY based on industry reports
- Competitors: 3 major players (InvestAI, SmartVC, VCGenius)
- Sentiment: Moderately positive, some skepticism about AI in finance

───────────────────────────────────────────────────────

[Task 2: Bull Agent]
Reviewing market research...

This is a MASSIVE opportunity! Here's why:

[Tool Call: ExaSearchTool(query="AI VC market growth 2025")]
Found 5 sources confirming AI adoption in VC accelerating:
- McKinsey: "AI in VC to grow 50% annually through 2027"
- PitchBook: "VCs investing $2B+ in AI deal sourcing tools"

BULL CASE FOR MARKET:
1. **Large, fast-growing market**: $5B → $7B next year (40% growth)
2. **Strong tailwinds**: Institutional investors NEED AI to scale deal flow
3. **Only 3 competitors**: Room for strong #2 or #3 player
4. **Pricing power**: Competitors charge $30-50k, healthy margins
5. **Validation**: 60% positive HN sentiment shows market demand

This is an early-stage, high-growth market with clear demand!

───────────────────────────────────────────────────────

[Task 3: Bear Agent]
Reviewing market research and Bull's arguments...

Hold on. Let me verify some of these claims.

[Tool Call: ApifyScraperTool(url="investai.com/customers")]
InvestAI has 500+ customers listed. That's significant market share.

[Tool Call: HackerNewsSearchTool(query="AI investment failures")]
Found discussions on AI failures in finance:
- "AI can't replace judgment in early-stage investing"
- "Most AI deal sourcing tools fail to deliver ROI"

BEAR CASE FOR MARKET:
1. **Market is already crowded**: 3 well-funded competitors is NOT "only 3"
   - InvestAI: $100M raised, 500+ customers, strong brand
   - SmartVC: $30k pricing undercuts potential margins

2. **Skepticism in target market**: 40% negative HN sentiment means...
   - VCs are skeptical of AI replacing judgment
   - "AI fatigue" - everyone claims AI now

3. **Pricing pressure incoming**: SmartVC at $30k creates race to bottom

4. **Bull's "tailwinds" are hype**: Yes, VCs talk about AI...
   - But adoption ≠ purchase decisions
   - Many VCs testing free tools, not paying $50k

5. **Market timing risk**: If we invest now and AI hype fades...
   - Customers might churn when budgets tighten
   - We're at peak hype, not sustainable demand

REALITY: This is a competitive, uncertain market with execution risk.

───────────────────────────────────────────────────────

[Task 4: Risk Assessor]
Reviewing market discussion...

TOP MARKET RISKS:

| Risk | Likelihood (1-5) | Impact (1-5) | Mitigation |
|------|-----------------|--------------|------------|
| Market timing (AI hype fade) | 4 | 5 | Launch before hype fades |
| Competitive pressure | 5 | 4 | Differentiate on product |
| Pricing race to bottom | 4 | 4 | Focus on value, not price |
| Customer adoption slower than expected | 3 | 4 | Get 10+ customers pre-raise |
| Regulatory (AI in finance) | 2 | 5 | Monitor SEC guidance |

FAILURE SCENARIO:
"Acme launches in crowded market. InvestAI drops price to $25k to defend market share.
SmartVC already at $30k. Acme forced to price at $20k to compete. Unit economics break.
Burn increases. Can't raise next round. Shutdown in 18 months."

MONITORING PLAN:
- Track competitor pricing monthly
- Monitor HN sentiment quarterly
- Watch for new entrants (CB Insights alerts)

═══════════════════════════════════════════════════════
ROUND 2: TEAM DISCUSSION
═══════════════════════════════════════════════════════

[Task 5: Founder Evaluator]
Evaluating founding team...

[Tool Call: GitHubAnalyzerTool(username="acme_founder")]
GitHub Analysis:
- 1,200 commits in last year
- Top languages: Python (60%), JavaScript (30%)
- Notable repos: ml-research (500 stars), data-pipeline (200 stars)
- Code quality: HIGH (good documentation, tests, clean architecture)

[Tool Call: ExaSearchTool(query="Acme founder background")]
Founder: Jane Smith
- PhD in Machine Learning (Stanford)
- 3 years at Google Brain
- Published 5 papers on recommendation systems

FOUNDER EVALUATION:

SCORE: 7/10

STRENGTHS:
✅ Strong technical background (PhD, Google Brain experience)
✅ Active coder (1200 commits shows hands-on, not just manager)
✅ Relevant domain expertise (ML + recommendation systems applicable to deal sourcing)
✅ Code quality is excellent (professional engineering standards)

CONCERNS:
⚠️ NO business co-founder - who handles sales/marketing/operations?
⚠️ NO prior startup experience - first-time founder
⚠️ NO domain expertise in VC/finance - building for market they don't know
⚠️ Only 3 years work experience - relatively junior

RED FLAGS:
🚩 No clear GTM plan visible (no head of sales/marketing)
🚩 Solo founder risk - if Jane leaves, company fails

───────────────────────────────────────────────────────

[Task 6: Bull Agent]
This team can EXECUTE! Here's why:

BULL CASE FOR TEAM:
1. **Technical excellence**: Jane is a Stanford PhD with Google pedigree
   - Her code quality is exceptional (I'd invest in her as an engineer)
   - 1200 commits = she's building, not just pitching

2. **Domain expertise IS relevant**:
   - Recommendation systems → deal sourcing is pattern matching
   - Google Brain experience → can build production ML systems

3. **First-time founder is fine**:
   - Many successful founders had no prior startup experience
   - Technical founders learn business, easier than reverse

4. **She can hire**:
   - With our funding, she can recruit VP Sales, Head of GTM
   - Technical founder + strong hires often works

Jane is the type of founder VCs dream about: brilliant, technical, and executing.

───────────────────────────────────────────────────────

[Task 7: Bear Agent]
Let's be realistic about execution risk...

BEAR CASE FOR TEAM:
1. **Solo technical founder = highest failure rate**:
   - Data shows solo founders have 50% lower success rate
   - Jane needs co-founder, not employee #5 as "VP Sales"

2. **No VC/finance expertise is CRITICAL flaw**:
   - Building for VCs without being a VC = dangerous
   - How does she know what VCs actually need vs. want?

3. **"Can hire sales" is not a plan**:
   - Who will hire this person? Jane has no experience hiring sales
   - When will they hire? After raising? Too late.
   - Great sales leaders don't join single-person startups

4. **Google Brain ≠ startup skills**:
   - Large company experience rarely translates
   - Jane has never worn multiple hats
   - Never had to hustle for customers

5. **Bull's "she can learn business" is wishful thinking**:
   - Technical → business is 3-5 year learning curve
   - We're investing now, need execution NOW

REALITY: 7/10 technical talent, 2/10 execution ability. High team risk.

───────────────────────────────────────────────────────

[Task 8: Risk Assessor]
EXECUTION RISKS:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Solo founder burnout | 4 | 5 | Require co-founder or strong #2 hire |
| Failed sales hiring | 4 | 5 | Mandate VP Sales hire as funding condition |
| Market misjudgment (non-VC building for VCs) | 4 | 4 | Require 10 VC customer interviews |
| Technical debt from speed | 3 | 3 | Acceptable early-stage risk |

CONSENSUS: Team has strong technical capability but concerning execution gaps.

═══════════════════════════════════════════════════════
[Rounds 3-4 continue similarly...]
═══════════════════════════════════════════════════════

ROUND 5: FINAL DECISION
═══════════════════════════════════════════════════════

[Task 17: Lead Partner]
After reviewing all 16 tasks across 4 discussion rounds...

DECISION: PASS

CONFIDENCE: HIGH

RATIONALE:
This investment has THREE compounding risks that make it a PASS:

1. **Market Risk (Medium-High)**:
   - Crowded space with well-funded competitors
   - Pricing pressure from SmartVC at $30k
   - Market timing risk (AI hype might fade)
   - Bear's competitive analysis is more compelling than Bull's "only 3 competitors"

2. **Team Risk (HIGH)**:
   - Solo technical founder with no business co-founder
   - No sales/GTM expertise or hire
   - First-time founder building for market they don't understand
   - This is a structural problem, not fixable quickly

3. **Product Risk (Medium)** [from Round 3]:
   - Unclear differentiation vs. InvestAI
   - "AI-powered" is table stakes, not moat
   - Copyable by competitors in 6-12 months

KEY INSIGHT:
Any ONE of these risks might be acceptable.
THREE TOGETHER is too much for early-stage investment.

Bear's arguments consistently stronger than Bull's across all rounds:
- Market: Bear's competitive analysis > Bull's "huge opportunity" claims
- Team: Bear's execution concerns > Bull's "can hire" optimism
- Product: Bear's moat analysis > Bull's feature lists

INVESTMENT RECOMMENDATION:
PASS now, but REVISIT IN 6-12 MONTHS if Jane:
1. Adds business co-founder OR hires VP Sales with strong track record
2. Gets to $50k MRR with 10+ paying customers (proves market demand)
3. Demonstrates clear product differentiation (not just "AI-powered")

DISSENTING OPINIONS ACKNOWLEDGED:
Bull made valid points about market size and Jane's technical talent.
However, execution risk outweighs opportunity size at this stage.

This is a "NOT YET" not a "NEVER" - we'd love to invest after de-risking.

═══════════════════════════════════════════════════════
```

This example shows:
- ✅ Evidence-based debate (tools used throughout)
- ✅ Multiple perspectives (Bull vs Bear on each topic)
- ✅ Focused discussions (each round stays on topic)
- ✅ Synthesis at end (Lead Partner weighs all evidence)
- ✅ Realistic VC analysis (matches real partner discussions)

---

**End of Architecture Document**

This architecture creates an AI system that thinks like real VCs:
- Structured yet flexible
- Evidence-based yet opinionated
- Comprehensive yet efficient
- Fast yet thorough
- Automated yet human-like

Perfect for demonstrating how AI can augment (not replace) human decision-making.
