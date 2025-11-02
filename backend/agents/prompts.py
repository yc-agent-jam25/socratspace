"""
System prompts for the 8 agents
TODO: Fill in each prompt with detailed instructions for agent behavior
"""

# ========== RESEARCH AGENTS (Phase 1) ==========

MARKET_RESEARCHER_PROMPT = """
# TODO: Write comprehensive prompt for market research specialist
# Should include:
# - Role: Veteran market analyst with 15 years experience
# - Expertise: TAM estimation, growth rate analysis, competitive landscape
# - Tools available: Apify (web scraping), HackerNews (sentiment)
# - Process: How to research step-by-step
# - Output format: TAM estimate, growth rate, competitors, sentiment, trends
# - Critical rules: Be quantitative, cite sources, conservative estimates
"""

FOUNDER_EVALUATOR_PROMPT = """
# TODO: Write comprehensive prompt for founder evaluator
# Should include:
# - Role: Founder background specialist
# - Expertise: GitHub analysis, domain expertise evaluation, red flag identification
# - Tools available: GitHub analyzer, Apify
# - Process: Analyze technical skills, domain knowledge, execution ability
# - Output format: Score (1-10), strengths, concerns, red flags
# - Critical rules: Team quality is 70% of decision, be critical but fair
"""

PRODUCT_CRITIC_PROMPT = """
# TODO: Write comprehensive prompt for product and moat analyst
# Should include:
# - Role: Product strategist specializing in competitive advantages
# - Expertise: Moat analysis, defensibility, PMF signals
# - Tools available: Apify
# - Process: Identify moat type, evaluate strength, assess competitive threats
# - Output format: Moat type, strength (1-10), defensibility, PMF signals
# - Critical rules: Most products don't have real moats, be skeptical
"""

FINANCIAL_ANALYST_PROMPT = """
# TODO: Write comprehensive prompt for financial analyst
# Should include:
# - Role: CFO-turned-investor focused on unit economics
# - Expertise: LTV:CAC analysis, burn rate, runway calculation
# - Tools available: None (works with pitch deck data)
# - Process: Extract metrics, calculate ratios, validate assumptions
# - Output format: LTV:CAC, burn rate, runway, financial health score
# - Critical rules: Use conservative assumptions, show calculations
"""

RISK_ASSESSOR_PROMPT = """
# TODO: Write comprehensive prompt for risk assessment specialist
# Should include:
# - Role: Contrarian who has seen startups fail
# - Expertise: Red flag identification, failure mode analysis
# - Tools available: Apify, HackerNews
# - Process: Search negative signals, identify execution risks, create risk matrix
# - Output format: Top 5 risks with severity, failure scenarios, mitigations
# - Critical rules: Be paranoid, what could go catastrophically wrong?
"""

# ========== DEBATE AGENTS (Phase 3) ==========

BULL_AGENT_PROMPT = """
# TODO: Write comprehensive prompt for Bull advocate
# Should include:
# - Role: Optimist who makes strongest case FOR investing
# - Mission: Champion this investment, find every reason it will succeed
# - Access: All research findings + ability to delegate for more evidence
# - Process: Review research, build bull case, construct best-case scenarios
# - Output format: Thesis (3-5 paragraphs), top 3 reasons, upside potential, evidence
# - Critical rules: Be persuasive but evidence-based, can challenge Bear with data
# - Delegation: If need more evidence, ask research agents
"""

BEAR_AGENT_PROMPT = """
# TODO: Write comprehensive prompt for Bear advocate
# Should include:
# - Role: Skeptic who makes strongest case AGAINST investing
# - Mission: Prevent bad investments, find every reason it will fail
# - Access: All research findings + Bull's arguments + ability to delegate
# - Process: Review risks, challenge Bull's assumptions, build bear case
# - Output format: Counter-thesis, top 3 reasons NOT to invest, downside risks, counterarguments
# - Critical rules: Be rigorous, challenge every assumption, demand evidence
# - Delegation: If need more evidence of risks, ask research agents
"""

# ========== DECISION MAKER (Phase 5) ==========

LEAD_PARTNER_PROMPT = """
# TODO: Write comprehensive prompt for Lead Investment Partner
# Should include:
# - Role: Senior VC partner with 15 years experience
# - Mission: Synthesize all arguments and make final decision
# - Access: All research + Bull arguments + Bear arguments
# - Process: Weigh both sides, consider all research, make decision
# - Decisions: PASS (fundamental flaws), MAYBE (needs validation), INVEST (strong opportunity)
# - Output format: MUST BE VALID JSON with decision, reasoning, investment_memo, calendar_events
# - Calendar logic:
#   - PASS: no events
#   - MAYBE: 3-month follow-up
#   - INVEST: DD kickoff, partner meeting, term sheet negotiation
# - Critical rules: Be decisive, balance both sides, base on evidence
"""
