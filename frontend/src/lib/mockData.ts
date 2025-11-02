/**
 * Mock data for simulation
 */

import type { AgentMessage, Decision, CompanyData } from './types';

export const mockCompanyData: CompanyData = {
  company_name: 'AI Safety Labs',
  website: 'https://aisafetylabs.ai',
  founder_github: 'johndoe',
  industry: 'AI Safety',
  product_description: 'Building advanced AI alignment tools for enterprise applications'
};

// Agent message templates
const agentMessageTemplates = {
  market_researcher: [
    'Analyzing Total Addressable Market (TAM)...',
    'TAM estimated at $5.2B with 30% YoY growth. Key competitors: Anthropic, OpenAI Safety Team, Alignment Research Center.',
    'Market sentiment on HackerNews is highly positive. 47 mentions in the last month, 89% positive sentiment.',
    'Competitive landscape: 3 major players, significant white space in enterprise segment.'
  ],
  founder_evaluator: [
    'Analyzing founder GitHub profile...',
    'Founder has 127 repositories, 2,400+ contributions in the last year. Strong focus on ML/AI safety.',
    'Previous experience at Google Brain and DeepMind. Published 8 papers on AI alignment.',
    'Team execution score: 9/10. Strong technical background with proven track record.'
  ],
  product_critic: [
    'Evaluating product defensibility...',
    'Product has strong network effects and proprietary datasets. Tech stack: Python, PyTorch, custom alignment algorithms.',
    'Moat strength: 7/10. Defensibility comes from unique data and research partnerships.',
    'Product-market fit signals: 12 enterprise pilots, 4 signed LOIs, average contract value $180K/year.'
  ],
  financial_analyst: [
    'Analyzing unit economics...',
    'LTV:CAC ratio of 5.2:1 (healthy). Current burn rate: $85K/month with 14 months runway.',
    'Revenue model: SaaS subscription with enterprise licensing. Current MRR: $42K, growing 25% MoM.',
    'Financial health score: 8/10. Strong unit economics, need to extend runway.'
  ],
  risk_assessor: [
    'Identifying potential risks...',
    'Top risks: 1) Regulatory uncertainty in AI safety, 2) Competition from well-funded players, 3) Talent acquisition.',
    'Red flags: Limited runway, dependence on 2 key customers for 60% of revenue.',
    'Risk severity: MEDIUM. Manageable with proper execution and follow-on funding.'
  ],
  bull_agent: [
    'Building the bull case...',
    '🐂 STRONG BUY: Market growing 30% YoY, exceptional team with Google/DeepMind background, proven product-market fit.',
    'Upside potential: 10x in 3 years. Enterprise AI safety is a $50B+ market by 2028. Early mover advantage is critical.',
    'This team can execute. Strong unit economics (LTV:CAC 5.2:1) and clear path to profitability.'
  ],
  bear_agent: [
    'Building the bear case...',
    '🐻 CAUTION: Only 14 months runway, 60% revenue concentration risk, facing well-funded competition.',
    'Regulatory uncertainty could kill the market. OpenAI and Anthropic are entering this space with 100x more resources.',
    'Valuation risk: At current traction, difficult to justify post-money valuation expectations.'
  ],
  lead_partner: [
    'Synthesizing all arguments...',
    'Weighing bull vs bear cases against research findings...',
    'Final decision reached. Generating investment memo...'
  ]
};

export const generateMockMessages = (agentId: string, count: number): AgentMessage[] => {
  const templates = agentMessageTemplates[agentId as keyof typeof agentMessageTemplates] || ['Working...'];
  const messages: AgentMessage[] = [];
  
  for (let i = 0; i < Math.min(count, templates.length); i++) {
    messages.push({
      agent: agentId,
      message: templates[i],
      message_type: 'info',
      timestamp: Date.now() + i * 1000
    });
  }
  
  return messages;
};

const investmentMemo = `# Investment Memo: AI Safety Labs

## Executive Summary

AI Safety Labs is building enterprise AI alignment tools targeting the rapidly growing AI safety market. The company has demonstrated strong product-market fit with 12 enterprise pilots and $42K MRR growing at 25% MoM. The founding team brings exceptional credentials from Google Brain and DeepMind.

**Recommendation: INVEST** with conditions on extending runway and diversifying customer base.

## Market Opportunity

- **TAM**: $5.2B, growing at 30% YoY
- **Market Position**: Early mover in enterprise AI safety segment
- **Competitive Landscape**: 3 major competitors (Anthropic, OpenAI Safety, ARC), but significant white space in enterprise
- **Market Sentiment**: Highly positive (89% positive mentions on HackerNews)

## Team Assessment

**Strengths:**
- Founders: Ex-Google Brain and DeepMind engineers
- Published research: 8 papers on AI alignment
- Technical depth: 2,400+ GitHub contributions, strong ML/AI focus
- Execution score: 9/10

**Concerns:**
- Team of 4, need to scale hiring
- Heavy technical focus, may need commercial leadership

## Product & Moat

**Product:**
- SaaS platform for enterprise AI alignment
- Proprietary datasets and custom algorithms
- Python/PyTorch stack with custom alignment tools

**Defensibility (7/10):**
- Network effects from enterprise partnerships
- Proprietary research and datasets
- First-mover advantage in enterprise segment

**Product-Market Fit:**
- 12 active pilots
- 4 signed LOIs averaging $180K/year
- Strong customer retention and engagement

## Financial Analysis

**Unit Economics:**
- LTV:CAC: 5.2:1 (healthy)
- Current MRR: $42K (+25% MoM)
- Average Contract Value: $180K/year
- Gross Margin: ~80%

**Burn & Runway:**
- Monthly burn: $85K
- Current runway: 14 months
- Need: $2-3M to extend to 24+ months

**Revenue Model:**
- SaaS subscriptions (monthly/annual)
- Enterprise licensing
- Professional services (implementation)

## Risk Analysis

**Key Risks:**
1. **Revenue Concentration** (HIGH): 60% revenue from 2 customers
2. **Limited Runway** (MEDIUM): Only 14 months, need fundraise
3. **Competition** (MEDIUM): Well-funded players entering space
4. **Regulatory** (LOW-MEDIUM): AI safety regulation uncertainty

**Mitigation:**
- Diversify customer base (underway)
- Raise bridge round immediately
- Leverage first-mover advantage
- Engage with regulators early

## Bull Case

Market is exploding (30% YoY growth), team is world-class (Google/DeepMind pedigree), and product-market fit is proven (12 pilots, 25% MoM growth). Early mover advantage in enterprise AI safety is worth 10x in 3 years. Unit economics are stellar (5.2:1 LTV:CAC). This is a category-defining company.

**Upside Scenario:** $50M+ ARR in 3 years, acquired by major tech company or IPO path.

## Bear Case

Limited runway (14 months) creates financing risk. Revenue concentration (60% from 2 customers) is dangerous. Anthropic and OpenAI have 100x more resources and are entering this space. Regulatory uncertainty could kill the market. Valuation expectations may be too high for current traction.

**Downside Scenario:** Runway runs out before next fundraise, customers churn, competition crushes margins.

## Decision Rationale

Despite legitimate concerns around runway and concentration risk, the opportunity is compelling:

1. **Market Timing**: AI safety is critical and growing rapidly
2. **Team Quality**: World-class technical team with proven execution
3. **Traction**: Real revenue and customer validation
4. **Economics**: Strong unit economics support scalability

The risks are manageable with proper execution and bridge financing.

## Next Steps

**Investment Terms:**
- Amount: $2M Series Seed
- Valuation: $15M post-money
- Use of funds: 60% product, 20% sales, 20% operations

**Conditions:**
- Diversify customer base (target 5+ customers for 80% revenue)
- Hire VP Sales within 90 days
- Achieve $100K MRR by month 6

**Timeline:**
- Due diligence kickoff: Tomorrow
- Partner decision meeting: Next week
- Term sheet negotiation: 2 weeks
- Close: 4 weeks
`;

export const mockDecisions: Record<'INVEST' | 'MAYBE' | 'PASS', Decision> = {
  INVEST: {
    decision: 'INVEST',
    reasoning: 'Strong team with Google/DeepMind background, proven product-market fit with 12 pilots and $42K MRR growing 25% MoM, excellent unit economics (LTV:CAC 5.2:1), and massive market opportunity ($5.2B TAM, 30% YoY growth). While revenue concentration and limited runway are concerns, these are manageable with proper execution and bridge financing. The first-mover advantage in enterprise AI safety justifies the investment.',
    investment_memo: investmentMemo,
    calendar_events: [
      {
        title: 'DD Kickoff: AI Safety Labs',
        start_time: new Date(Date.now() + 86400000).toISOString(), // Tomorrow
        end_time: new Date(Date.now() + 86400000 + 3600000).toISOString(),
        attendees: ['Partners', 'Founders', 'Legal Team'],
        description: 'Deep dive into tech, legal, and financial due diligence'
      },
      {
        title: 'Partner Meeting: AI Safety Labs',
        start_time: new Date(Date.now() + 604800000).toISOString(), // Next week
        end_time: new Date(Date.now() + 604800000 + 3600000).toISOString(),
        attendees: ['All Partners'],
        description: 'Review DD findings and make final investment decision'
      },
      {
        title: 'Term Sheet Negotiation: AI Safety Labs',
        start_time: new Date(Date.now() + 1209600000).toISOString(), // 2 weeks
        end_time: new Date(Date.now() + 1209600000 + 3600000).toISOString(),
        attendees: ['Lead Partner', 'Founders'],
        description: 'Negotiate investment terms and finalize term sheet'
      }
    ]
  },
  MAYBE: {
    decision: 'MAYBE',
    reasoning: 'Interesting opportunity with strong technical team and solid product, but significant concerns around limited runway (14 months), high revenue concentration (60% from 2 customers), and intense competition. Market opportunity is real, but execution risk is high. Recommend waiting for more traction and customer diversification before investing.',
    investment_memo: investmentMemo.replace('INVEST', 'MAYBE'),
    calendar_events: [
      {
        title: 'Follow-up: AI Safety Labs',
        start_time: new Date(Date.now() + 7776000000).toISOString(), // 3 months
        end_time: new Date(Date.now() + 7776000000 + 1800000).toISOString(),
        attendees: ['Lead Partner', 'Founders'],
        description: 'Check progress on customer diversification and MRR growth'
      }
    ]
  },
  PASS: {
    decision: 'PASS',
    reasoning: 'While the team is strong and the market is attractive, the risks outweigh the opportunity at this stage. Critical concerns: (1) Only 14 months runway with high burn rate, (2) 60% revenue from just 2 customers creates existential risk, (3) Well-funded competitors (Anthropic, OpenAI) entering the space with 100x more resources, (4) Product defensibility is unclear. Recommend passing and revisiting if they achieve stronger traction and customer diversification.',
    investment_memo: investmentMemo.replace('INVEST', 'PASS'),
    calendar_events: []
  }
};

export const getMockDecision = (type: 'INVEST' | 'MAYBE' | 'PASS' = 'INVEST'): Decision => {
  return mockDecisions[type];
};

