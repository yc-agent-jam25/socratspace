/**
 * Debate Viewer Component
 * Main component that orchestrates the debate visualization
 * TODO: Implement real-time debate viewer
 */

import React, { useEffect, useState } from 'react';
import type { CompanyData, AgentMessage, Decision, Agent } from '../lib/types';
import useWebSocket from '../hooks/useWebSocket';
import AgentCard from './AgentCard';
import PhaseIndicator from './PhaseIndicator';
import DecisionPanel from './DecisionPanel';

interface DebateViewerProps {
  sessionId: string;
  companyData: CompanyData;
  onReset: () => void;
}

const agents: Agent[] = [
  { id: 'market_researcher', name: 'Market Researcher', color: '#1976d2' },
  { id: 'founder_evaluator', name: 'Founder Evaluator', color: '#388e3c' },
  { id: 'product_critic', name: 'Product Critic', color: '#f57c00' },
  { id: 'financial_analyst', name: 'Financial Analyst', color: '#7b1fa2' },
  { id: 'risk_assessor', name: 'Risk Assessor', color: '#d32f2f' },
  { id: 'bull_agent', name: 'Bull Agent', color: '#2e7d32' },
  { id: 'bear_agent', name: 'Bear Agent', color: '#c62828' },
  { id: 'lead_partner', name: 'Lead Partner', color: '#1565c0' }
];

const DebateViewer: React.FC<DebateViewerProps> = ({ sessionId, companyData, onReset }) => {
  const [currentPhase, _setCurrentPhase] = useState<string>('research');
  const [agentMessages, _setAgentMessages] = useState<AgentMessage[]>([]);
  const [decision, _setDecision] = useState<Decision | null>(null);

  // TODO: Connect WebSocket
  const { lastMessage } = useWebSocket(`${import.meta.env.VITE_WS_URL || 'ws://localhost:8000'}/ws`);

  useEffect(() => {
    // TODO: Handle WebSocket messages
    // Types: phase_change, agent_message, decision, error
  }, [lastMessage]);

  return (
    <div>
      <h2>Analyzing: {companyData.company_name}</h2>
      <p>Session: {sessionId}</p>
      <button onClick={onReset}>New Analysis</button>

      <PhaseIndicator currentPhase={currentPhase} />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
        {agents.map(agent => (
          <AgentCard
            key={agent.id}
            agent={agent}
            messages={agentMessages.filter(m => m.agent === agent.id)}
            active={currentPhase === 'research'}
          />
        ))}
      </div>

      {decision && <DecisionPanel decision={decision} />}
    </div>
  );
};

export default DebateViewer;
