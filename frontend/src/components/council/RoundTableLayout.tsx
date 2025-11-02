/**
 * RoundTableLayout Component
 * Circular arrangement for research phase (5 agents)
 */

import React from 'react';
import { Box } from '@mui/material';
import type { Agent, AgentMessage } from '../../lib/types';
import AgentAvatar from '../agents/AgentAvatar';
import MessageBubble from '../messages/MessageBubble';
import ConnectionLine from '../messages/ConnectionLine';

interface AgentPosition {
  agent: Agent;
  x: number;
  y: number;
  angle: number;
}

interface RoundTableLayoutProps {
  agents: Agent[];
  messages: AgentMessage[];
  activeAgents: string[];
  onAgentClick?: (agent: Agent) => void;
  containerWidth: number;
  containerHeight: number;
}

const RoundTableLayout: React.FC<RoundTableLayoutProps> = ({
  agents,
  messages,
  activeAgents,
  onAgentClick,
  containerWidth,
  containerHeight,
}) => {
  // Calculate circular positions for agents
  const calculatePositions = (): AgentPosition[] => {
    const centerX = containerWidth / 2;
    const centerY = containerHeight / 2;
    const radius = Math.min(containerWidth, containerHeight) * 0.35;

    return agents.map((agent, index) => {
      // Start from top and go clockwise
      const angle = (index * (360 / agents.length) - 90) * (Math.PI / 180);
      return {
        agent,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        angle: angle * (180 / Math.PI),
      };
    });
  };

  const positions = calculatePositions();

  // Get agent status
  const getAgentStatus = (agentId: string): 'idle' | 'thinking' | 'speaking' | 'done' => {
    const agentMessages = messages.filter(m => m.agent === agentId);
    const isActive = activeAgents.includes(agentId);
    
    if (!isActive && agentMessages.length > 0) return 'done';
    if (isActive) {
      const lastMessage = agentMessages[agentMessages.length - 1];
      const timeSinceLastMessage = Date.now() - (typeof lastMessage?.timestamp === 'number' ? lastMessage.timestamp : 0);
      return timeSinceLastMessage < 2000 ? 'speaking' : 'thinking';
    }
    return 'idle';
  };

  // Get recent messages for display
  const getRecentMessages = () => {
    return messages.slice(-3); // Show last 3 messages
  };

  const recentMessages = getRecentMessages();

  return (
    <Box
      sx={{
        position: 'relative',
        width: '100%',
        height: '100%',
        minHeight: 600,
      }}
    >
      {/* Central icon/logo */}
      <Box
        sx={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
          width: 80,
          height: 80,
          borderRadius: '50%',
          background: 'rgba(59, 130, 246, 0.1)',
          border: '2px solid rgba(59, 130, 246, 0.3)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '2rem',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 0 30px rgba(59, 130, 246, 0.2)',
        }}
      >
        🏛️
      </Box>

      {/* Connection lines between active agents */}
      {positions.map((fromPos, i) => 
        positions.slice(i + 1).map((toPos) => {
          const fromActive = activeAgents.includes(fromPos.agent.id);
          const toActive = activeAgents.includes(toPos.agent.id);
          
          if (fromActive && toActive) {
            return (
              <ConnectionLine
                key={`${fromPos.agent.id}-${toPos.agent.id}`}
                from={{ x: fromPos.x, y: fromPos.y }}
                to={{ x: toPos.x, y: toPos.y }}
                color={fromPos.agent.color}
                animated
                dashed
              />
            );
          }
          return null;
        })
      )}

      {/* Agent avatars */}
      {positions.map(({ agent, x, y }) => (
        <Box
          key={agent.id}
          sx={{
            position: 'absolute',
            left: x,
            top: y,
            transform: 'translate(-50%, -50%)',
            transition: 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
            zIndex: 10,
          }}
        >
          <AgentAvatar
            name={agent.name}
            color={agent.color}
            status={getAgentStatus(agent.id)}
            size="medium"
            showLabel
            onClick={() => onAgentClick?.(agent)}
          />
        </Box>
      ))}

      {/* Message bubbles */}
      {recentMessages.map((message, index) => {
        const agentPos = positions.find(p => p.agent.id === message.agent);
        if (!agentPos) return null;

        // Position messages near their agents with slight offset
        const offsetAngle = (agentPos.angle + 45) * (Math.PI / 180);
        const offsetDistance = 120;
        const messageX = agentPos.x + Math.cos(offsetAngle) * offsetDistance;
        const messageY = agentPos.y + Math.sin(offsetAngle) * offsetDistance;

        return (
          <Box
            key={`${message.agent}-${message.timestamp}-${index}`}
            sx={{
              position: 'absolute',
              left: messageX,
              top: messageY,
              transform: 'translate(-50%, -50%)',
              zIndex: 5,
              animation: 'fadeIn 0.5s ease-out',
            }}
          >
            <MessageBubble
              message={message}
              agentColor={agentPos.agent.color}
              agentName={agentPos.agent.name}
            />
          </Box>
        );
      })}
    </Box>
  );
};

export default RoundTableLayout;

