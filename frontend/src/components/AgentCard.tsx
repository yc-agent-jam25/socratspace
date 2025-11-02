/**
 * Agent Card Component
 * Displays individual agent status and messages
 * TODO: Implement agent visualization
 */

import React from 'react';
import type { Agent, AgentMessage } from '../lib/types';

interface AgentCardProps {
  agent: Agent;
  messages: AgentMessage[];
  active: boolean;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, messages, active }) => {
  // TODO: Implement card display
  // TODO: Show agent name, color, status
  // TODO: Display latest message
  // TODO: Highlight when active

  return (
    <div style={{ borderLeft: `4px solid ${agent.color}`, opacity: active ? 1 : 0.7 }}>
      <h3>{agent.name}</h3>
      <p>TODO: Display latest message</p>
      <p>{messages.length} messages</p>
    </div>
  );
};

export default AgentCard;
