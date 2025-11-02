# MCP System Architecture

## Overview

This application uses **Metorial's MCP (Model Context Protocol)** platform to give AI agents access to external tools and data sources. Instead of building custom integrations for each service, we deploy pre-built MCP servers on Metorial and call them via natural language.

## What is MCP?

**Model Context Protocol (MCP)** is a standard for connecting LLMs to external tools and data sources. Think of it as a plugin system for AI agents.

**Metorial** is a hosted platform that:
- Deploys MCP servers (like HackerNews, GitHub, Apify, Exa)
- Provides an SDK to call them
- Handles authentication, scaling, and rate limiting

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│          CrewAI Agents (8 agents)                   │
│  (Market Researcher, Bull, Bear, Lead Partner, etc) │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ Uses tools during tasks
                   │
┌──────────────────▼──────────────────────────────────┐
│         CrewAI Tool Wrappers (4 tools)              │
│   - HackerNewsSearchTool                            │
│   - GitHubAnalyzerTool                              │
│   - ApifyScraperTool                                │
│   - ExaSearchTool                                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ Calls via mcp_client
                   │
┌──────────────────▼──────────────────────────────────┐
│            MetorialClient                           │
│         (tools/mcp_client.py)                       │
│  - Translates tool calls to natural language        │
│  - Routes to correct MCP server                     │
│  - Returns formatted results                        │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ Uses Metorial SDK
                   │
┌──────────────────▼──────────────────────────────────┐
│          Metorial Platform (Cloud)                  │
│  - Hosts MCP servers                                │
│  - Uses LLM to interpret requests                   │
│  - Executes tools and returns results               │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ Calls actual APIs
                   │
┌──────────────────▼──────────────────────────────────┐
│         External Services                           │
│  - HackerNews API                                   │
│  - GitHub API                                       │
│  - Apify (web scraping)                             │
│  - Exa (search engine)                              │
└─────────────────────────────────────────────────────┘
```

## Key Components

### 1. MetorialClient (`tools/mcp_client.py`)

**Purpose**: Central client that all tools use to communicate with Metorial MCP servers.

**Key Features**:
- **Singleton pattern**: One global `mcp_client` instance
- **Deployment ID mapping**: Maps friendly names ("hackernews") to deployment IDs ("svd_xxx")
- **Natural language interface**: Converts tool parameters to natural language prompts
- **LLM-powered**: Uses GPT-4o to interpret requests and call the right MCP tools

**How it works**:

```python
# Initialize with Metorial SDK
self.metorial = Metorial(api_key=settings.metorial_api_key)
self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

# Map friendly names to deployment IDs
self.deployment_ids = {
    "hackernews": settings.mcp_hackernews_id,  # svd_0mhh9nkzweERz8yndQOSXO
    "github": settings.mcp_github_id,
    "apify": settings.mcp_apify_id,
    "exa": settings.mcp_exa_id,
}

# Call MCP with natural language
async def call_mcp(mcp_name, tool_name, parameters, natural_message):
    deployment_id = self.deployment_ids[mcp_name]

    # Construct message for LLM
    message = f"{natural_message}\n\nParameters: {json.dumps(parameters)}"

    # Use Metorial SDK to run
    result = await self.metorial.run(
        message=message,
        server_deployments=[deployment_id],
        client=self.openai_client,
        model="gpt-4o"
    )

    return result  # RunResult with .text and .steps
```

### 2. CrewAI Tool Wrappers (`tools/*.py`)

**Purpose**: Wrap MCP calls in CrewAI's `BaseTool` interface so agents can use them.

**Pattern Used**:

```python
class HackerNewsSearchTool(BaseTool):
    name: str = "HackerNews Search"
    description: str = "Searches HackerNews for discussions..."
    args_schema: Type[BaseModel] = HackerNewsSearchInput

    def _run(self, query: str, limit: int = 10) -> str:
        async def search():
            # Call MCP with natural language instruction
            result = await mcp_client.call_mcp(
                mcp_name="hackernews",
                tool_name="search_stories",
                parameters={"query": query, "limit": limit},
                natural_message=f"""
                Search HackerNews for discussions about "{query}".
                Find the top {limit} stories with points, comments, and sentiment.
                """
            )

            # Format result for agent
            return f"=== HackerNews Results ===\n{result.text}"

        return asyncio.run(search())
```

**Why this design?**
- CrewAI agents expect synchronous `_run()` methods
- MCP calls are async
- Solution: Wrap async call in `asyncio.run()`

### 3. MCP Servers (Deployed on Metorial)

**Deployed Servers**:
1. **HackerNews MCP** (`svd_0mhh9nkzweERz8yndQOSXO`)
   - Tools: `get_top_stories`, `get_best_stories`, `get_item`
   - Purpose: Search HN for company/tech discussions

2. **GitHub MCP** (`svd_0mhh9vs9o6XLezyEVO8SFP`)
   - Tools: `get_repository`, `search_repositories`, `get_user`
   - Purpose: Analyze founder GitHub profiles

3. **Apify MCP** (`svd_0mhh9wgz0d3EkqJwI4dWls`)
   - Tools: Web scraping actors
   - Purpose: Scrape competitor websites, pricing pages

4. **Exa MCP** (`svd_0mhcakg7680J7ENuiEWKAq`)
   - Tools: Neural search engine
   - Purpose: Search for company information, market research

### 4. Configuration (`config.py` + `.env`)

**Environment Variables**:
```bash
# Metorial Platform
METORIAL_API_KEY=metorial_sk_xxx
METORIAL_BASE_URL=https://api.metorial.com/v1

# MCP Deployment IDs (from Metorial dashboard)
MCP_HACKERNEWS_ID=svd_0mhh9nkzweERz8yndQOSXO
MCP_GITHUB_ID=svd_0mhh9vs9o6XLezyEVO8SFP
MCP_APIFY_ID=svd_0mhh9wgz0d3EkqJwI4dWls
MCP_EXA_ID=svd_0mhcakg7680J7ENuiEWKAq

# OpenAI (used by Metorial SDK to interpret requests)
OPENAI_API_KEY=sk-xxx
```

**Pydantic Settings Class**:
```python
class Settings(BaseSettings):
    metorial_api_key: str
    metorial_base_url: str = "https://api.metorial.com/v1"

    mcp_hackernews_id: str
    mcp_github_id: str
    mcp_apify_id: str
    mcp_exa_id: Optional[str] = None

    openai_api_key: str

    model_config = ConfigDict(env_file=".env", case_sensitive=False)
```

## How a Tool Call Works (Step-by-Step)

Let's trace what happens when a Bull Agent searches HackerNews:

### Step 1: Agent Invokes Tool

```python
# Inside CrewAI task execution
bull_agent.use_tool(
    tool="HackerNews Search",
    parameters={"query": "AI investment tools", "limit": 10}
)
```

### Step 2: Tool Wrapper Receives Call

```python
# HackerNewsSearchTool._run() is called
def _run(self, query: str, limit: int = 10) -> str:
    async def search():
        result = await mcp_client.call_mcp(
            mcp_name="hackernews",
            tool_name="search_stories",
            parameters={"query": "AI investment tools", "limit": 10},
            natural_message="""
            Search HackerNews for discussions about "AI investment tools".
            Find the top 10 stories with points, comments, and sentiment.
            """
        )
        return result.text

    return asyncio.run(search())
```

### Step 3: MCP Client Routes to Metorial

```python
# MetorialClient.call_mcp()
deployment_id = "svd_0mhh9nkzweERz8yndQOSXO"  # HackerNews MCP

message = """
Search HackerNews for discussions about "AI investment tools".
Find the top 10 stories with points, comments, and sentiment.

Parameters: {"query": "AI investment tools", "limit": 10}
"""

result = await self.metorial.run(
    message=message,
    server_deployments=[deployment_id],
    client=self.openai_client,
    model="gpt-4o"
)
```

### Step 4: Metorial Platform Executes

Metorial's platform:
1. Receives the natural language request
2. Uses GPT-4o to understand what tools to call
3. Sees HackerNews MCP has tools like `get_top_stories`, `search_stories`
4. Calls the appropriate tool(s) with correct parameters
5. Formats the response

### Step 5: HackerNews API Called

The HackerNews MCP server:
1. Calls HackerNews API: `https://hacker-news.firebaseio.com/v0/topstories.json`
2. Fetches story details for top stories
3. Filters by relevance to "AI investment tools"
4. Returns structured data

### Step 6: Results Flow Back

```
HackerNews API Response
    ↓
HackerNews MCP Server (formats data)
    ↓
Metorial Platform (GPT-4o summarizes)
    ↓
MetorialClient (receives RunResult)
    ↓
HackerNewsSearchTool (formats for agent)
    ↓
Bull Agent (uses results in argument)
```

### Step 7: Agent Uses Results

```python
# Bull Agent receives:
"""
=== HackerNews Community Analysis ===
Search Query: "AI investment tools"
Stories Analyzed: 10

Top Stories Found:
1. "AI-Powered Investment Platform Raises $50M" (342 points, 156 comments)
   Link: https://news.ycombinator.com/item?id=12345
   Sentiment: Positive - Developers excited about automation

2. "Why AI Investment Tools Will Fail" (89 points, 234 comments)
   Link: https://news.ycombinator.com/item?id=67890
   Sentiment: Skeptical - Concerns about over-reliance on AI

...

Overall Sentiment: Mixed (60% positive, 40% skeptical)
Key Themes: Automation potential, regulatory concerns, trust issues
Red Flags: Several comments mention "too early for AI in finance"
"""

# Agent incorporates this into their argument
```

## Design Decisions & Trade-offs

### ✅ Benefits of This Architecture

1. **No API Integration Code**
   - Don't need to learn HackerNews API, GitHub API, Apify API, etc.
   - Metorial handles authentication, rate limits, pagination

2. **Natural Language Interface**
   - Agents can be flexible in how they use tools
   - LLM interprets requests, chooses best tool approach

3. **Easy to Add New Tools**
   - Deploy new MCP on Metorial
   - Add deployment ID to config
   - Create thin wrapper tool
   - Done!

4. **Hosted & Scalable**
   - Metorial handles infrastructure
   - No server management
   - Built-in rate limiting

### ⚠️ Trade-offs

1. **Additional Latency**
   - Extra LLM call (GPT-4o interprets request)
   - ~1-2 seconds overhead per tool call

2. **Cost**
   - Metorial charges per API call
   - Plus OpenAI tokens for interpretation
   - ~$0.0001 per call (negligible for hackathon)

3. **Less Control**
   - Can't fine-tune exact API calls
   - Dependent on Metorial's LLM interpretation
   - Debugging is harder (blackbox)

4. **Network Dependency**
   - Requires internet connection
   - If Metorial is down, tools don't work

### Why We Chose This

For a **hackathon project**, the benefits outweigh trade-offs:
- ✅ Faster development (hours vs days)
- ✅ Focus on agent logic, not API integrations
- ✅ Easy to demo (just works)
- ⚠️ Latency acceptable for demo
- ⚠️ Cost negligible for short hackathon

For **production**, you might want:
- Direct API integrations for critical tools
- Keep MCP for less critical/exploratory tools
- Cache results to reduce costs

## How to Add a New MCP Tool

### 1. Deploy MCP on Metorial

1. Go to [metorial.com](https://metorial.com)
2. Navigate to "Connect" → "Deployments"
3. Click "Deploy MCP Server"
4. Choose from marketplace (e.g., "LinkedIn MCP", "Crunchbase MCP")
5. Get deployment ID (starts with `svd_`)

### 2. Add to Config

```python
# .env
MCP_LINKEDIN_ID=svd_new_deployment_id

# config.py
class Settings(BaseSettings):
    mcp_linkedin_id: Optional[str] = None
    ...
```

### 3. Update MCP Client

```python
# tools/mcp_client.py
self.deployment_ids = {
    "hackernews": settings.mcp_hackernews_id,
    "github": settings.mcp_github_id,
    "apify": settings.mcp_apify_id,
    "exa": settings.mcp_exa_id,
    "linkedin": settings.mcp_linkedin_id,  # ← Add this
}
```

### 4. Create Tool Wrapper

```python
# tools/linkedin_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from tools.mcp_client import mcp_client
import asyncio

class LinkedInSearchInput(BaseModel):
    person_name: str = Field(..., description="Name of person to search")

class LinkedInSearchTool(BaseTool):
    name: str = "LinkedIn Search"
    description: str = "Searches LinkedIn for professional profiles"
    args_schema: Type[BaseModel] = LinkedInSearchInput

    def _run(self, person_name: str) -> str:
        async def search():
            result = await mcp_client.call_mcp(
                mcp_name="linkedin",
                tool_name="search_person",
                parameters={"person_name": person_name},
                natural_message=f"""
                Search LinkedIn for professional profile of {person_name}.
                Get their current role, company, experience, and education.
                """
            )
            return result.text

        return asyncio.run(search())
```

### 5. Assign to Agents

```python
# agents/definitions.py
from tools.linkedin_tool import LinkedInSearchTool

founder_evaluator = Agent(
    role="Founder Evaluator",
    tools=[
        GitHubAnalyzerTool(),
        LinkedInSearchTool(),  # ← Add to agent
    ],
    ...
)
```

Done! The agent can now use LinkedIn data.

## Debugging Tips

### Check MCP Client Logs

```python
# tools/mcp_client.py uses Python logging
logger.info(f"Calling {mcp_name}.{tool_name} with params: {parameters}")
logger.info(f"MCP call successful: {mcp_name}.{tool_name}")
```

Run with logging enabled:
```bash
python -m logging.basicConfig(level=logging.INFO)
python test_hackernews_tool.py
```

### Test Tool Directly

```python
# test_hackernews_tool.py
from tools.hackernews_tool import HackerNewsSearchTool

tool = HackerNewsSearchTool()
result = tool._run("AI investment", limit=5)
print(result)
```

### Check Metorial Dashboard

1. Go to metorial.com → Dashboard
2. View recent API calls
3. See request/response logs
4. Check error messages

### Common Issues

**Error: "Deployment ID not found"**
- Check `.env` has correct `MCP_*_ID` values
- Verify deployment IDs start with `svd_`

**Error: "401 Unauthorized"**
- Check `METORIAL_API_KEY` in `.env`
- Regenerate key if needed

**Error: "OpenAI API key required"**
- Check `OPENAI_API_KEY` in `.env`
- Metorial SDK needs this to interpret requests

**Tool returns empty results**
- MCP server might not support that query
- Try simpler/different query
- Check Metorial dashboard for errors

## Cost Estimation

**Per Tool Call**:
- Metorial API: ~$0.00005
- OpenAI (GPT-4o for interpretation): ~$0.00005
- Total: **~$0.0001 per call**

**Typical Analysis**:
- 8 agents × 2-3 tool calls each = 16-24 calls
- Cost per analysis: **~$0.002-0.003** (less than a penny!)

**Hackathon Budget**:
- 100 test runs = $0.30
- Totally negligible

## Security Notes

1. **API Keys in .env**
   - Never commit `.env` to git
   - `.gitignore` already configured

2. **Metorial API Key**
   - Treat like a password
   - Can be regenerated if leaked

3. **OpenAI API Key**
   - Set spending limits in OpenAI dashboard
   - Monitor usage

4. **MCP Deployment IDs**
   - Not secret, but keep private
   - Can be changed if abused

## References

- **Metorial Documentation**: https://docs.metorial.com
- **MCP Specification**: https://modelcontextprotocol.io
- **CrewAI Tools**: https://docs.crewai.com/tools
- **Metorial Python SDK**: https://pypi.org/project/metorial/
