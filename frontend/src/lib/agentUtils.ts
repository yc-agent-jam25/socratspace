/**
 * Utility functions for agent name normalization
 * Maps backend agent role names to frontend agent IDs
 */

/**
 * Map backend agent role names to frontend agent IDs
 *
 * Backend sends role names like "Market Research Specialist"
 * Frontend uses IDs like "market_researcher"
 */
export const normalizeAgentName = (agentName: string): string => {
  const roleToIdMap: Record<string, string> = {
    // Backend role names from backend/agents/definitions.py
    'Market Research Specialist': 'market_researcher',
    'Founder Evaluator': 'founder_evaluator',
    'Product Critic': 'product_critic',
    'Financial Analyst': 'financial_analyst',
    'Risk Assessor': 'risk_assessor',
    'Bull Advocate': 'bull_agent',
    'Bear Advocate': 'bear_agent',
    'Lead Investment Partner': 'lead_partner',

    // Fallback: also support lowercase IDs directly (in case backend changes)
    'market_researcher': 'market_researcher',
    'founder_evaluator': 'founder_evaluator',
    'product_critic': 'product_critic',
    'financial_analyst': 'financial_analyst',
    'risk_assessor': 'risk_assessor',
    'bull_agent': 'bull_agent',
    'bear_agent': 'bear_agent',
    'lead_partner': 'lead_partner',

    // System messages (from backend orchestrator)
    'system': 'system',
  };

  // If agent name is not found in map, default to 'system' instead of 'unknown'
  return roleToIdMap[agentName] || 'system';
};

/**
 * Agent role to ID mapping (for reference)
 */
export const AGENT_ROLE_MAP = {
  'Market Research Specialist': 'market_researcher',
  'Founder Evaluator': 'founder_evaluator',
  'Product Critic': 'product_critic',
  'Financial Analyst': 'financial_analyst',
  'Risk Assessor': 'risk_assessor',
  'Bull Advocate': 'bull_agent',
  'Bear Advocate': 'bear_agent',
  'Lead Investment Partner': 'lead_partner',
} as const;
