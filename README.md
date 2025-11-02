# 🏛️ VC Council - AI Investment Committee

**Tagline:** *8 AI agents debate your investment decisions. From pitch deck to calendar invite in 5 minutes.*

**Built for:** YC Agent Jam '25 Hackathon

---

## 📖 Table of Contents

1. [Overview](#-overview)
2. [The Problem We're Solving](#-the-problem-were-solving)
3. [How It Works](#-how-it-works---the-intuitive-explanation)
4. [The 8-Agent System](#-the-8-agent-system)
5. [Technical Architecture](#-technical-architecture--why-we-built-it-this-way)
6. [System Design Patterns](#-system-design-patterns)
7. [Implementation Guide](#-implementation-guide)
8. [Demo & Presentation](#-demo--presentation)
9. [Post-Hackathon Potential](#-post-hackathon-potential)

---

## 🎯 Overview

VC Council is a multi-agent AI system that revolutionizes investment decision-making. Instead of one AI giving you an answer, **8 specialized agents** conduct parallel research, engage in adversarial debate, and produce comprehensive investment memos—all in under 5 minutes.

**What makes it unique:**
- **Adversarial debate** between Bull and Bear agents surfaces blind spots
- **Multi-perspective analysis** reduces bias and catches what single agents miss
- **End-to-end workflow** from analysis to automated calendar scheduling
- **Real-time visualization** of agents debating like a courtroom

**Tech Stack:**
- Backend: Python FastAPI with custom multi-agent orchestrator
- Frontend: React + TypeScript with real-time WebSocket updates
- AI: OpenAI GPT-4 or Anthropic Claude
- MCPs: Apify, GitHub, HackerNews, Google Drive, Google Calendar (via Metorial)

---

## 🔥 The Problem We're Solving

### **The Current Reality:**

1. **VCs make $100K+ decisions in 30-minute meetings**
   - Limited time for due diligence
   - Rely on gut feeling and pattern matching
   - Miss critical details under time pressure

2. **Single-perspective analysis has blind spots**
   - Confirmation bias (seeing what you want to see)
   - Missing domain expertise (can't be expert in everything)
   - Groupthink in investment committees

3. **Manual due diligence takes weeks**
   - Research competitors manually
   - Check founder backgrounds on LinkedIn/GitHub
   - Read market reports
   - Each bad hire/investment costs $50K-100K+

4. **Follow-up tasks fall through the cracks**
   - Forget to schedule follow-up calls
   - Miss important check-in dates
   - Lose track of pipeline companies

### **Our Solution:**

**VC Council provides:**
- ✅ **Multi-perspective analysis in 5 minutes** (not weeks)
- ✅ **Adversarial debate** that surfaces both opportunities AND risks
- ✅ **Automated research** across web, GitHub, HackerNews, news
- ✅ **Smart calendar scheduling** based on decision
- ✅ **Investment memos that write themselves** with evidence and reasoning

---

## 💡 How It Works - The Intuitive Explanation

### **Think of it like a real investment committee meeting:**

**Scenario:** A startup applies for funding. You have their pitch deck and website.

**Traditional approach:**
1. One analyst reviews materials (4 hours)
2. Writes memo (2 hours)
3. Partners discuss in meeting (1 hour)
4. Someone manually schedules follow-ups
**Total: 7+ hours, single perspective**

**VC Council approach:**
1. Upload pitch deck, paste URLs
2. Watch 8 specialist agents research simultaneously (2 min)
3. Watch them debate the decision (3 min)
4. Get investment memo + automated calendar events
**Total: 5 minutes, 8 perspectives**

### **The Magic Happens in 5 Phases:**

```
Phase 1: RESEARCH (90 seconds)
├─ Market Researcher: Scraping competitors, market size
├─ Founder Evaluator: Analyzing GitHub, LinkedIn
├─ Product Critic: Examining product, tech stack
├─ Financial Analyst: Checking unit economics
└─ Risk Assessor: Searching for red flags
   (All happening simultaneously!)

Phase 2: FINDINGS (60 seconds)
├─ Each agent presents their key findings
└─ Think: "Here's what I discovered"

Phase 3: DEBATE (90 seconds)
├─ Bull Agent: "This will be HUGE because..."
├─ Bear Agent: "This will FAIL because..."
└─ They argue back and forth with evidence
   (Think: Courtroom debate with prosecuting vs. defending attorneys)

Phase 4: CROSS-EXAMINATION (60 seconds)
├─ Other agents challenge Bull and Bear
├─ "But what about X?"
└─ "Your evidence doesn't support that claim"
   (Think: Expert witnesses challenging the lawyers)

Phase 5: DECISION (30 seconds)
├─ Lead Partner synthesizes all arguments
├─ Makes decision: PASS / MAYBE / INVEST
├─ Generates investment memo
└─ Creates calendar events automatically
```

### **Why This Works Better:**

**1. Parallel Research = Speed**
- Traditional: One person researches sequentially (slow)
- VC Council: 5 agents research simultaneously (10x faster)

**2. Adversarial Debate = Catches Blind Spots**
- Traditional: Everyone agrees too quickly (groupthink)
- VC Council: Bull and Bear MUST argue opposite sides
- Result: You see both the opportunity AND the risks

**3. Multi-Perspective = Reduces Bias**
- Traditional: One analyst's opinion dominates
- VC Council: 8 different expert perspectives
- Result: More balanced, less biased decisions

**4. Automated Follow-ups = Nothing Falls Through Cracks**
- Traditional: Manually create calendar events
- VC Council: Smart scheduling based on decision
  - PASS → No events (move on)
  - MAYBE → Follow-up in 3 months + reminder
  - INVEST → Full due diligence schedule (3 meetings auto-created)

---

## 🤖 The 8-Agent System

### **Why 8 Agents? Why These Specific Roles?**

We designed the system like a real VC firm's investment committee:

### **The Research Team (Agents 1-5)**
These agents work in **parallel** to gather all the data.

#### **1. Market Researcher**
- **Role:** "Is this market big enough?"
- **What they do:**
  - Scrapes competitor websites (Apify)
  - Searches HackerNews for industry discussions
  - Estimates Total Addressable Market (TAM)
  - Identifies key competitors
- **Output:** Market size, growth rate, competitive landscape
- **Why we need them:** VCs need to know market potential

#### **2. Founder Evaluator**
- **Role:** "Can this team actually execute?"
- **What they do:**
  - Analyzes GitHub contributions (code quality, activity)
  - Scrapes LinkedIn for background (previous companies)
  - Checks for domain expertise
  - Looks for red flags (job hopping, conflicts)
- **Output:** Founder quality score, strengths, concerns
- **Why we need them:** Team is 70% of investment decision

#### **3. Product Critic**
- **Role:** "Is this product defensible?"
- **What they do:**
  - Scrapes product website, documentation
  - Analyzes tech stack (if GitHub available)
  - Evaluates moat (what prevents copycats?)
  - Checks for product-market fit signals
- **Output:** Defensibility rating, moat analysis, risks
- **Why we need them:** Product must have sustainable advantage

#### **4. Financial Analyst**
- **Role:** "Do the unit economics work?"
- **What they do:**
  - Parses metrics from pitch deck
  - Calculates LTV:CAC ratio
  - Estimates burn rate and runway
  - Validates revenue model
- **Output:** Financial health score, unit economics
- **Why we need them:** Must be financially viable

#### **5. Risk Assessor**
- **Role:** "What could go wrong?"
- **What they do:**
  - Scrapes news for negative articles
  - Searches HackerNews for critical comments
  - Identifies failure scenarios
  - Creates risk matrix
- **Output:** Critical risks, red flags, failure modes
- **Why we need them:** Must know downside before investing

### **The Debate Team (Agents 6-7)**
These agents **argue opposite sides** to surface all angles.

#### **6. Bull Agent (Optimist)**
- **Role:** "Make the strongest case FOR investing"
- **What they do:**
  - Reviews all positive findings from research team
  - Constructs best-case scenarios
  - Emphasizes strengths and opportunities
  - Argues why this could be a unicorn
- **Output:** Bull case with evidence, upside potential
- **Why we need them:** Need someone to champion the opportunity

#### **7. Bear Agent (Pessimist)**
- **Role:** "Make the strongest case AGAINST investing"
- **What they do:**
  - Reviews all negative findings and risks
  - Constructs worst-case scenarios
  - Emphasizes weaknesses and threats
  - Argues why this will fail
- **Output:** Bear case with evidence, downside risks
- **Why we need them:** Must hear the contrarian view

**Why adversarial debate?**
- Humans naturally seek confirming evidence (confirmation bias)
- By forcing agents to argue opposite sides, we surface ALL perspectives
- This is how courts work: prosecution vs. defense reveals truth

### **The Decision Maker (Agent 8)**

#### **8. Lead Partner**
- **Role:** "Synthesize and decide"
- **What they do:**
  - Reads all research findings
  - Weighs Bull vs Bear arguments
  - Considers all expert opinions
  - Makes final call with clear reasoning
  - Generates investment memo
  - Creates calendar events based on decision
- **Output:** PASS / MAYBE / INVEST + reasoning + memo + calendar
- **Why we need them:** Someone must make the final call

---

## 🏗️ Technical Architecture – Why We Built It This Way

### **The Big Decision: Framework vs. Custom**

We researched all major multi-agent frameworks:

| Framework | Verdict | Reasoning |
|-----------|---------|-----------|
| **LangGraph** | ❌ Too complex | State machines are powerful but overkill for 24 hours. Steep learning curve. |
| **AutoGen** | ❌ Being deprecated | Microsoft is replacing it with Agent Framework. Don't build on dying tech. |
| **CrewAI** | ⚠️ Could work | Easy to start, but built on LangChain (extra dependency). Less control over debate protocol. |
| **Custom** | ✅ **Our choice** | Full control, no framework overhead, tailored exactly to our needs. |

**Why custom orchestrator wins for hackathons:**
1. **Speed**: No time to learn framework quirks
2. **Control**: Debate protocol is unique, frameworks don't fit perfectly
3. **Performance**: No framework overhead
4. **Simplicity**: Easier to debug and demo

**What we borrowed from frameworks:**
- State management patterns from **LangGraph** (immutable state)
- Message passing from **AutoGen** (pub/sub communication)
- Event-driven architecture from **production systems**

---

## 🎨 System Design Patterns

### **Pattern 1: Debate-Based Consensus**

**What it is:**
Instead of agents working independently and voting, agents **engage in structured debate** where they:
- Present arguments
- Challenge each other
- Refine their positions
- Build toward consensus

**Why we use it:**
- Surfaces non-obvious insights through discussion
- Reduces blind spots (each agent catches what others miss)
- More realistic (mimics how humans make decisions)

**How it works in our system:**
```
Research Phase: Agents gather data independently
         ↓
Findings Phase: Agents present "Here's what I found"
         ↓
Debate Phase: Bull says "Invest!" Bear says "Don't!"
         ↓
Cross-Exam: Other agents ask "But what about X?"
         ↓
Decision: Lead Partner weighs all arguments
```

**Research source:** [Microsoft AutoGen Multi-Agent Debate](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/multi-agent-debate.html)

---

### **Pattern 2: Event-Driven Architecture**

**What it is:**
Components communicate by publishing events that others subscribe to, rather than calling each other directly.

**Why we use it:**
- **Loose coupling**: Agents don't need to know about each other
- **Real-time UI**: Frontend subscribes to events and updates live
- **Fault tolerance**: If one component fails, others keep working
- **Scalability**: Easy to add new subscribers

**How it works:**

```python
# Agent publishes event
await event_bus.publish("research_complete", {
    "agent": "market_researcher",
    "findings": {...}
})

# Orchestrator subscribes
event_bus.subscribe("research_complete",
    lambda data: state_manager.add_findings(data))

# UI subscribes (WebSocket)
event_bus.subscribe("research_complete",
    lambda data: websocket.send(data))
```

**Real-world analogy:**
- Traditional: Phone tree (A calls B, B calls C, C calls D)
- Event-driven: Group text (anyone can post, everyone sees it)

**Benefits for our demo:**
- UI updates in real-time as agents work
- If GitHub MCP fails, other agents still complete
- Easy to add logging, metrics without touching agent code

---

### **Pattern 3: Immutable State Management**

**What it is:**
State is never modified in place. Instead, we create a new copy with changes.

**Why we use it:**
- **Predictable**: Always know what changed and when
- **Debuggable**: Can replay entire debate from state history
- **Thread-safe**: No race conditions
- **Time-travel**: Can go back to any previous state

**How it works:**

```python
# BAD: Mutating state directly
state["phase"] = "debate"  # Hard to track changes

# GOOD: Immutable update
new_state = state_manager.update(phase="debate")  # Creates new copy
```

**Under the hood:**
```python
class StateManager:
    def __init__(self, initial_state):
        self._state = initial_state
        self._history = [initial_state]  # Keep all versions

    def update(self, **changes):
        new_state = deepcopy(self._state)  # Copy current state
        for key, value in changes.items():
            new_state[key] = value  # Apply changes
        self._state = new_state
        self._history.append(new_state)  # Save to history
        return new_state
```

**Why this matters:**
- Can show judges: "Here's the exact state when Bull agent challenged Bear"
- If demo breaks, can replay from any point
- Makes debugging 10x easier

**Borrowed from:** [LangGraph State Management](https://docs.langchain.com/oss/python/langgraph/overview)

---

### **Pattern 4: Hybrid Orchestration**

**What it is:**
We mix different orchestration patterns depending on the phase:

| Phase | Pattern | Why |
|-------|---------|-----|
| Research | **Parallel** | Maximize speed (5 agents at once) |
| Findings | **Sequential** | Clear presentation order |
| Debate | **Turn-taking** | Bull and Bear alternate |
| Cross-Exam | **Group chat** | Any agent can speak |
| Decision | **Hierarchical** | Lead Partner has final say |

**Why hybrid?**
- Each phase has different needs
- Parallel for speed, sequential for clarity
- More flexible than pure hierarchical or pure parallel

**Comparison:**

```
Pure Hierarchical (like a company):
  CEO → VP → Manager → Worker
  (Slow, but clear chain of command)

Pure Parallel (like a swarm):
  Agent1, Agent2, Agent3 all work independently
  (Fast, but chaotic)

Our Hybrid:
  Research phase: Parallel (fast!)
  Debate phase: Turn-taking (clear!)
  Decision: Hierarchical (decisive!)
```

---

### **Pattern 5: Shared Context with Message Passing**

**What it is:**
Agents access shared read-only context but communicate through explicit messages.

**Why this hybrid approach:**

**Shared Context** (read-only):
- Company info (website, founders, etc.)
- Other agents' findings
- Conversation history

**Message Passing** (challenges/responses):
- "I challenge your claim about market size"
- "Here's my counter-evidence"
- "I agree with Bear agent on this point"

**Why not pure message passing?**
- Too verbose (agents would spend time asking for basic info)
- Slower (extra round-trips)

**Why not pure shared memory?**
- Less traceable (hard to see who influenced who)
- No explicit debate (agents just write to same doc)

**Our hybrid:**
```python
class Agent:
    def __init__(self, shared_context, event_bus):
        self.context = shared_context  # Read other agents' findings
        self.event_bus = event_bus     # Send challenges/messages

    async def execute(self):
        # Read from shared context
        market_data = self.context.get_findings("market_researcher")

        # Send message via event bus
        await self.event_bus.publish("challenge", {
            "from": "bear_agent",
            "to": "bull_agent",
            "message": "Your TAM estimate is too high"
        })
```

---

## 🏛️ Detailed System Architecture

### **The Big Picture**

```
┌──────────────────────────────────────────────────────────────┐
│                    USER UPLOADS PITCH DECK                    │
│                    (Website, GitHub, PDF)                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                         │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              DEBATE ORCHESTRATOR                        │  │
│  │  "The conductor of the orchestra"                      │  │
│  │  - Manages 5 phases                                    │  │
│  │  - Enforces turn-taking                                │  │
│  │  - Handles timeouts                                    │  │
│  └────┬─────────────────────────────┬─────────────────────┘  │
│       │                             │                         │
│       ▼                             ▼                         │
│  ┌─────────┐                   ┌────────┐                    │
│  │  EVENT  │◄─────────────────►│ STATE  │                    │
│  │   BUS   │                   │MANAGER │                    │
│  │(Pub/Sub)│                   │(State) │                    │
│  └────┬────┘                   └───┬────┘                    │
│       │                            │                          │
│       ▼                            ▼                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │           AGENT EXECUTOR                             │    │
│  │  "Runs the 8 agents with their specialized prompts" │    │
│  │                                                      │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │    │
│  │  │Agent1│ │Agent2│ │Agent3│ │Agent4│ ...          │    │
│  │  │Market│ │Found.│ │Prodct│ │Financ│              │    │
│  │  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘              │    │
│  └─────┼────────┼────────┼────────┼───────────────────┘    │
│        │        │        │        │                          │
│        └────────┴────────┴────────┘                          │
│                  │                                            │
│                  ▼                                            │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         MCP INTEGRATION LAYER                        │    │
│  │  "Abstracts away the complexity of MCP calls"       │    │
│  │                                                      │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │    │
│  │  │Apify │ │GitHub│ │  HN  │ │GDrive│ │GCal  │    │    │
│  │  │Scrape│ │Code  │ │Sent. │ │Save  │ │Sched.│    │    │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │    │
│  └──────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────┘
                         │
                         │ WebSocket (Real-time)
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                  FRONTEND (React)                             │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐        │
│  │ Input Form  │  │Debate Viewer │  │Memo Display │        │
│  │Upload deck  │  │Watch agents  │  │Investment   │        │
│  │Paste URLs   │  │debate live   │  │memo + cal.  │        │
│  └─────────────┘  └──────────────┘  └─────────────┘        │
└───────────────────────────────────────────────────────────────┘
```

### **Component Deep Dive**

#### **1. Debate Orchestrator**
**Job:** "The conductor who makes sure everyone plays at the right time"

**Responsibilities:**
- **Phase management**: Transitions from Research → Findings → Debate → Cross-Exam → Decision
- **Turn-taking**: Ensures agents speak in order (no chaos)
- **Timeout enforcement**: Each agent gets max 30 seconds (keeps demo moving)
- **Error recovery**: If agent fails, uses fallback or continues without them

**Why it's needed:**
Without orchestrator = chaos (agents talking over each other, stuck in loops)
With orchestrator = structured debate (clear flow, predictable timing)

**Code pattern:**
```python
class DebateOrchestrator:
    async def run_debate(self):
        await self._phase_1_research()   # Parallel execution
        await self._phase_2_findings()   # Sequential presentations
        await self._phase_3_debate()     # Turn-taking debate
        await self._phase_4_cross_exam() # Group discussion
        await self._phase_5_decision()   # Final decision
```

#### **2. State Manager**
**Job:** "The memory that tracks everything happening in the debate"

**What it stores:**
- Current phase (are we in debate? decision?)
- All agent findings (market data, founder eval, etc.)
- Conversation history (every message agents sent)
- Final outputs (decision, memo, calendar events)

**Why immutable?**
- Can replay entire debate (useful for debugging)
- No race conditions (multiple agents updating at once)
- Clear audit trail (exactly what changed when)

**Example:**
```python
# Initial state
state = {
    "phase": "research",
    "findings": {},
    "messages": []
}

# Agent completes research
state = state_manager.update(
    findings={"market_researcher": {...}}
)
# Now state has new findings, old state preserved in history

# Can access history
history = state_manager.get_history()  # See every state change
```

#### **3. Event Bus**
**Job:** "The announcement system - when something happens, everyone hears about it"

**How it works:**
```python
# Agent publishes event
event_bus.publish("agent_finished", {
    "agent": "market_researcher",
    "data": {...}
})

# Multiple subscribers react:
# 1. Orchestrator: "Move to next phase"
# 2. UI: "Update progress bar"
# 3. Logger: "Write to log file"
# 4. Metrics: "Record timing"
```

**Why it's powerful:**
- **Decoupling**: Agents don't know who's listening (don't care)
- **Real-time UI**: Frontend subscribes via WebSocket, updates instantly
- **Easy debugging**: Subscribe a logger to see everything happening

#### **4. Agent Executor**
**Job:** "The factory that creates and runs agents"

**What it does:**
1. Takes agent role (e.g., "market_researcher")
2. Loads specialized prompt for that role
3. Calls LLM (GPT-4/Claude) with prompt + context
4. Parses LLM response
5. Calls any tools needed (MCP integrations)
6. Returns structured findings

**Why separate executor?**
- **Reusability**: Same execution logic for all 8 agents
- **Error handling**: Retry logic in one place
- **Monitoring**: Track timing, costs, failures centrally

#### **5. MCP Integration Layer**
**Job:** "The translators who speak to external services"

**What it abstracts:**
- Connection management (auth, rate limits)
- Error handling (retry, fallbacks)
- Response parsing (different APIs, same interface)
- Caching (don't re-scrape same URL)

**Example:**
```python
# Agent just calls
findings = await mcp.apify.scrape(url)

# Behind the scenes:
# - Checks cache first
# - Connects to Metorial
# - Calls Apify MCP
# - Retries if fails
# - Returns clean data
```

---

## 💾 State Management - The Deep Dive

### **Why State Management is Critical**

**The problem:**
- 8 agents running in parallel
- Each finds different information
- Need to track who said what, when
- Must handle errors gracefully
- UI needs real-time updates

**Without proper state management:**
- Race conditions (two agents update same thing)
- Lost messages (agent says something, we forget)
- Debugging nightmare (no history of what happened)
- Inconsistent UI (shows different data than backend)

### **Our Solution: Immutable State with TypedDict**

**The State Schema:**

```python
from typing import TypedDict, List, Dict, Optional, Literal

class DebateState(TypedDict):
    """Complete state of one debate session"""

    # WHO: Which company are we analyzing?
    company: {
        "name": "Anthropic",
        "website": "anthropic.com",
        "founder_github": "github.com/founder"
    }

    # WHERE: What phase are we in?
    phase: "research" | "findings" | "debate" | "cross_exam" | "decision"

    # WHAT: What have agents discovered?
    findings: {
        "market_researcher": {
            "summary": "AI safety market is $5B...",
            "evidence": ["url1", "url2"]
        },
        "founder_evaluator": {...},
        # ... other agents
    }

    # SAID: What have agents said to each other?
    messages: [
        {
            "agent": "bull_agent",
            "content": "This will be huge because...",
            "timestamp": 1234567890,
            "evidence": ["url1"]
        },
        # ... more messages
    ]

    # DECIDED: Final decision
    decision: "INVEST" | "MAYBE" | "PASS" | None
    decision_reasoning: "Strong team, defensible moat...",
    investment_memo: "Full markdown memo...",
    calendar_events: [...]
}
```

**How updates work (immutable pattern):**

```python
# Step 1: Agent finishes research
state_manager.add_findings(
    agent="market_researcher",
    findings={...}
)

# Under the hood:
# 1. Copy entire state
# 2. Add new findings to copy
# 3. Save old state to history
# 4. Publish event "findings_added"
# 5. UI automatically updates
```

**Benefits we get:**

1. **Time-travel debugging:**
```python
# See state at any point in time
states = state_manager.get_history()
state_at_debate_start = states[10]  # What was state before debate?
```

2. **Replay entire debate:**
```python
for state in state_manager.get_history():
    print(f"Phase: {state['phase']}")
    print(f"Messages: {len(state['messages'])}")
    # Can recreate entire debate flow
```

3. **Thread-safe:**
```python
# Multiple agents can call this simultaneously
# No race conditions because we copy entire state
state_manager.add_findings(agent="agent1", ...)
state_manager.add_findings(agent="agent2", ...)
```

---

## 🔄 Communication Patterns

### **Pattern 1: Message Passing (Agent-to-Agent)**

**When agents challenge each other:**

```python
# Bear agent challenges Bull
await event_bus.publish("challenge", {
    "from": "bear_agent",
    "to": "bull_agent",
    "claim": "Market TAM is $5B",
    "challenge": "Your TAM estimate seems high. Gartner says $3B.",
    "evidence": ["gartner.com/report/123"]
})

# Bull agent receives challenge, responds
await event_bus.publish("response", {
    "from": "bull_agent",
    "to": "bear_agent",
    "response": "Gartner report is from 2023. IDC 2025 report shows $5B.",
    "evidence": ["idc.com/report/456"]
})
```

**Why explicit messages?**
- **Traceable**: Can see exactly who influenced who
- **Theatrical**: Makes great demo (courtroom vibes)
- **Debuggable**: Can replay conversation flow

### **Pattern 2: Shared Context (Read-Only)**

**When agents need background info:**

```python
class SharedContext:
    """All agents can read from here"""

    def get_company_info(self):
        return state_manager.state["company"]

    def get_other_findings(self, requesting_agent):
        # Agent can see what others found
        all_findings = state_manager.state["findings"]
        return {k: v for k, v in all_findings.items()
                if k != requesting_agent}

# Agent uses it
class BullAgent:
    async def execute(self):
        # Read what Market Researcher found
        market_data = self.context.get_findings("market_researcher")

        # Use it to build bull case
        bull_case = f"Market is growing {market_data['growth_rate']}"
```

**Why shared context?**
- **Efficiency**: Don't pass same company info 8 times
- **Consistency**: Everyone sees same data
- **Simple**: Just read, don't modify

---

## 🚀 Performance Optimizations

### **1. Parallel Execution**

**The problem:**
If we run 5 research agents sequentially: 5 × 30 sec = 2.5 minutes
Too slow for demo!

**The solution:**
Run them in parallel: max(30 sec) = 30 seconds
**5x faster!**

**Code:**
```python
# BAD: Sequential (slow)
for agent in research_agents:
    findings = await agent.execute()  # Wait for each one

# GOOD: Parallel (fast)
findings = await asyncio.gather(
    agent1.execute(),
    agent2.execute(),
    agent3.execute(),
    agent4.execute(),
    agent5.execute()
)  # All run simultaneously!
```

### **2. Caching MCP Responses**

**The problem:**
- Apify scraping same competitor site multiple times
- GitHub API rate limits
- Slow repeated calls

**The solution:**
Cache responses for 5 minutes

**Code:**
```python
class MCPCache:
    def __init__(self):
        self._cache = {}  # {url: (data, timestamp)}

    async def get_or_fetch(self, url, fetcher):
        # Check cache
        if url in self._cache:
            data, cached_at = self._cache[url]
            if time.time() - cached_at < 300:  # 5 min TTL
                return data

        # Cache miss - fetch fresh
        data = await fetcher(url)
        self._cache[url] = (data, time.time())
        return data
```

**Impact:**
- Faster demos (instant on retry)
- Lower costs (fewer API calls)
- Respects rate limits

### **3. Timeout Management**

**The problem:**
Agent gets stuck waiting for slow API = entire debate hangs

**The solution:**
Timeout + fallback

**Code:**
```python
async def execute_agent_with_timeout(agent, timeout=30):
    try:
        return await asyncio.wait_for(
            agent.execute(),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        # Use fallback response
        return {
            "agent": agent.role,
            "summary": "Analysis unavailable (timeout)",
            "confidence": 0.0
        }
```

**Impact:**
- Demo never hangs
- Graceful degradation (some agents fail, debate continues)
- Shows fault tolerance

---

## 📅 Calendar Integration - The Smart Part

### **Why This is Clever**

Most AI demos just give you text. We go further:
**Decision → Automated actions**

### **The Logic:**

**Decision: PASS**
```python
if decision == "PASS":
    # Do nothing - move on
    return []
```

**Decision: MAYBE**
```python
if decision == "MAYBE":
    return [
        # Check back in 3 months
        create_event(
            title="Follow-up: {company}",
            date=today + 90 days,
            duration=30 min,
            description="Check if they have traction"
        ),
        # Reminder 1 week before
        create_event(
            title="Reminder: Prepare for {company} call",
            date=today + 83 days,
            duration=15 min
        )
    ]
```

**Decision: INVEST**
```python
if decision == "INVEST":
    return [
        # Tomorrow: Kickoff due diligence
        create_event(
            title="DD Kickoff: {company}",
            date=tomorrow,
            duration=1 hour,
            attendees=[partners, founders],
            description="Deep dive: Tech, Legal, Financial"
        ),
        # Next week: Partner decision meeting
        create_event(
            title="Partner Meeting: {company}",
            date=today + 7 days,
            duration=1 hour,
            attendees=[partners],
            description="Review DD, make final decision"
        ),
        # 2 weeks: Negotiate terms
        create_event(
            title="Term Sheet Negotiation: {company}",
            date=today + 14 days,
            duration=1 hour,
            attendees=[lead_partner, founders],
            description="Negotiate investment terms"
        )
    ]
```

### **Why This Matters:**

**Traditional:**
1. AI gives recommendation
2. You read it
3. **You manually create 3 calendar events**
4. You manually share with attendees
5. 15 minutes of admin work

**VC Council:**
1. AI makes decision
2. **Calendar events appear automatically**
3. Attendees already invited
4. Documents already shared
5. **Zero admin work**

**This is the "wow" moment** in the demo - judges see real workflow automation, not just text generation.

---

## 📊 Project Structure

```
vc-council/
├── backend/
│   ├── main.py                          # FastAPI app
│   ├── config.py                        # Settings
│   │
│   ├── core/
│   │   ├── state_manager.py             # Immutable state
│   │   ├── event_bus.py                 # Pub/sub
│   │   └── shared_context.py            # Read-only context
│   │
│   ├── orchestration/
│   │   ├── orchestrator.py              # Debate coordinator
│   │   └── phases.py                    # Phase implementations
│   │
│   ├── agents/
│   │   ├── base_agent.py                # Base class
│   │   ├── market_researcher.py         # Individual agents
│   │   ├── founder_evaluator.py
│   │   ├── product_critic.py
│   │   ├── financial_analyst.py
│   │   ├── risk_assessor.py
│   │   ├── bull_agent.py
│   │   ├── bear_agent.py
│   │   └── lead_partner.py
│   │
│   ├── mcps/
│   │   ├── base_client.py               # Base MCP client
│   │   ├── apify_client.py              # Web scraping
│   │   ├── github_client.py             # Code analysis
│   │   ├── hackernews_client.py         # Sentiment
│   │   ├── gdrive_client.py             # Document storage
│   │   └── gcalendar_client.py          # Event scheduling
│   │
│   ├── services/
│   │   ├── memo_generator.py            # Investment memos
│   │   └── calendar_service.py          # Calendar logic
│   │
│   └── api/
│       ├── websockets.py                # Real-time updates
│       └── endpoints.py                 # REST API
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx                      # Main app
│   │   ├── components/
│   │   │   ├── InputForm.tsx            # Upload interface
│   │   │   ├── DebateViewer.tsx         # Watch debate
│   │   │   ├── AgentCard.tsx            # Agent display
│   │   │   ├── ResearchPhase.tsx        # Phase 1 UI
│   │   │   ├── DebatePhase.tsx          # Phase 3 UI
│   │   │   ├── DecisionPanel.tsx        # Final decision
│   │   │   ├── InvestmentMemo.tsx       # Memo viewer
│   │   │   └── CalendarEvents.tsx       # Show events
│   │   └── lib/
│   │       ├── api.ts                   # Backend calls
│   │       ├── websocket.ts             # Real-time
│   │       └── types.ts                 # TypeScript types
│   └── package.json
│
└── docs/
    ├── AGENT_PROMPTS.md                 # All 8 prompts
    ├── MCP_SETUP.md                     # Metorial config
    └── DEMO_SCRIPT.md                   # 5-min script
```

---

## 🎬 Demo & Presentation

### **5-Minute Demo Script**

**Minute 1: Hook (30s)**
- "VCs make $100K decisions in 30 minutes"
- "What if 8 AI agents could debate it in 5 minutes?"
- **Show title screen with 8 agents**

**Minute 2: Setup (30s)**
- Pick a well-known startup (e.g., "AI safety startup like Anthropic")
- Upload pitch deck
- Paste website URL, founder GitHub
- Click "Start Analysis"
- **Agents light up one by one**

**Minute 3: Phase 1-2 (60s)**
- **Research Phase:**
  - Show 5 agents scraping in parallel
  - Live logs: "Market Researcher: Found 3 competitors..."
  - "Founder Evaluator: Analyzing 47 GitHub repos..."
- **Findings Phase:**
  - Each agent presents in 10 seconds
  - Key insight from each appears on screen

**Minute 4: Phase 3-4 (60s)**
- **Debate Phase:**
  - Bull: "This will be huge! Market growing 30% YoY..."
  - Bear: "But competitor just raised $100M..."
  - Bull: "Our tech is 10x faster, that's the moat..."
  - Bear: "Speed isn't defensible, others will catch up..."
- **Cross-Exam:**
  - Risk Assessor: "Bull agent, what about the competitive threat?"
  - Financial Analyst: "Bear agent, unit economics are strong though..."

**Minute 5: Phase 5 + Magic (60s)**
- **Decision:**
  - Lead Partner: "After weighing all arguments..."
  - Decision appears: **"INVEST"**
  - Reasoning: "Strong team, defensible moat, $5B TAM"
- **Investment memo** generates (scroll through it)
- **THE WOW MOMENT:**
  - Calendar events appear automatically:
    - "DD Kickoff: Tomorrow at 10am"
    - "Partner Meeting: Next week"
    - "Term Sheet Negotiation: 2 weeks"
  - Show Google Calendar with events already created
  - Memo saved to Google Drive

**Final 30s: The Insight**
- "Single agent missed that competitor raised $100M"
- "Multi-agent debate caught it"
- **Show side-by-side comparison**
- "This is how AI should make high-stakes decisions"
- "Available for YC companies today"

### **Why This Demo Wins:**

1. **Theatrical**: Watching agents debate is engaging (like courtroom)
2. **Novel**: No one else has adversarial debate + calendar integration
3. **Practical**: Judges immediately see the business value
4. **Technical**: Shows sophisticated multi-agent coordination
5. **Complete**: Full workflow from input to automated action
6. **Live**: Real-time visualization builds tension

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- Metorial account with API key
- OpenAI or Anthropic API key

### **Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env:
#   METORIAL_API_KEY=your_key
#   OPENAI_API_KEY=your_key
#   METORIAL_DEPLOYMENT_IDS={"apify": "...", "github": "..."}

# Run backend
python main.py
```

### **Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env:
#   VITE_API_URL=http://localhost:8000

# Run development server
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## ⏱️ 24-Hour Build Timeline

**Hours 0-4: Core Infrastructure**
- ✅ State management (TypedDict + immutability)
- ✅ Event bus (pub/sub)
- ✅ Base agent class
- ✅ Orchestrator skeleton

**Hours 4-8: Agent Implementation**
- ✅ 8 agent prompts and logic
- ✅ LLM integration (OpenAI/Claude)
- ✅ Basic MCP integration (Apify + GitHub)

**Hours 8-12: Debate Logic**
- ✅ 5-phase orchestration
- ✅ Message passing between agents
- ✅ State transitions and validation

**Hours 12-16: Frontend**
- ✅ WebSocket integration
- ✅ Real-time debate viewer
- ✅ Agent cards and UI components

**Hours 16-20: Integration & Polish**
- ✅ Calendar integration
- ✅ Google Drive integration
- ✅ Error handling and retries

**Hours 20-24: Demo Prep**
- ✅ 3 demo scenarios
- ✅ Backup video
- ✅ Deploy to production
- ✅ Final testing

---

## 🎯 Post-Hackathon Potential

### **Immediate Opportunities**
1. **YC companies as beta users** (pitch at event)
2. **VC firms as customers** ($299/month per partner)
3. **Open-source the framework** (monetize enterprise features)

### **Product Roadmap**

**v1.1: More Agents**
- Legal specialist (contract review)
- IP specialist (patent analysis)
- Go-to-market specialist (distribution strategy)

**v1.2: Learning System**
- Agents improve from past decisions
- Learn from successful/failed investments
- Personalize to each VC firm's thesis

**v1.3: Integrations**
- Carta (cap table management)
- AngelList (deal flow)
- DocSend (track deck views)

**v2.0: White-Label**
- Corporate VC arms (Google Ventures, Intel Capital)
- Custom agents per firm
- Private deployment

### **Business Model**

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | 5 analyses/month, public memos |
| **Pro** | $299/month | Unlimited analyses, private memos, priority support |
| **Enterprise** | Custom | Custom agents, white-label, SLA, private deployment |

### **Market Size**

- 1,000+ VC firms in US
- 10,000+ angel investors
- 100+ corporate VC arms
- **TAM: $500M+ annually**

**Unit Economics:**
- CAC: $500 (inbound, YC network)
- LTV: $10,000+ (annual contract, 3+ year retention)
- LTV:CAC = 20:1 (excellent)

---

## 🙏 Acknowledgments

- **Metorial (YC F25)** - For the MCP platform that makes this possible
- **Y Combinator** - For hosting Agent Jam '25
- **OpenAI/Anthropic** - For the AI models powering the agents
- **Multi-agent research community** - For pioneering debate frameworks
- **Microsoft AutoGen** - For debate pattern inspiration
- **LangGraph** - For state management patterns

---

## 📞 Contact

**Built by:** [Your Name]
**For:** YC Agent Jam '25 Hackathon
**Email:** your.email@example.com
**GitHub:** github.com/yourusername/vc-council
**Demo:** [Coming Soon]

---

## 📚 Technical References

- [Microsoft AutoGen Multi-Agent Debate](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/multi-agent-debate.html)
- [LangGraph State Management](https://docs.langchain.com/oss/python/langgraph/overview)
- [Azure AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Event-Driven Multi-Agent Systems](https://www.confluent.io/blog/event-driven-multi-agent-systems/)
- [Debate-Based Consensus Implementation](https://medium.com/@edoardo.schepis/patterns-for-democratic-multi-agent-ai-debate-based-consensus-part-2-implementation-2348bf28f6a6)
- [Multi-Agent System Best Practices 2025](https://www.gocodeo.com/post/multi-agent-systems-in-ai-architecture)

---

**"Truth emerges from the clash of ideas. Let 8 agents debate your next investment."**

---

## 🎓 Appendix: Learning Resources

### **For Understanding Multi-Agent Systems:**
1. Start with [AutoGen Multi-Agent Debate](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/multi-agent-debate.html)
2. Read [Azure's AI Agent Patterns Guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
3. Watch the debate happen live in our demo

### **For Building Your Own:**
1. Study our `orchestration/orchestrator.py` file
2. See how agents communicate via `core/event_bus.py`
3. Understand state management in `core/state_manager.py`
4. Copy our patterns, improve them!

---

**Made with ❤️ for the AI agent community**
