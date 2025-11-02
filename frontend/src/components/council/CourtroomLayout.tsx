/**
 * CourtroomLayout Component
 * Debate layout with Bull vs Bear (courtroom style)
 */

import React from 'react';
import { Box, Typography } from '@mui/material';
import type { Agent, AgentMessage } from '../../lib/types';
import AgentAvatar from '../agents/AgentAvatar';
import MessageBubble from '../messages/MessageBubble';
import ConnectionLine from '../messages/ConnectionLine';

interface CourtroomLayoutProps {
  bullAgent: Agent;
  bearAgent: Agent;
  observerAgents: Agent[];
  messages: AgentMessage[];
  activeAgents: string[];
  onAgentClick?: (agent: Agent) => void;
  containerWidth: number;
  containerHeight: number;
}

const CourtroomLayout: React.FC<CourtroomLayoutProps> = ({
  bullAgent,
  bearAgent,
  observerAgents,
  messages,
  activeAgents,
  onAgentClick,
  containerWidth,
  containerHeight,
}) => {
  // Get agent status
  const getAgentStatus = (agentId: string): 'idle' | 'thinking' | 'speaking' | 'done' => {
    const agentMessages = messages.filter(m => m.agent === agentId);
    const isActive = activeAgents.includes(agentId);
    
    if (!isActive && agentMessages.length > 0) return 'done';
    if (isActive) {
      const lastMessage = agentMessages[agentMessages.length - 1];
      const timeSinceLastMessage = Date.now() - (lastMessage?.timestamp || 0);
      return timeSinceLastMessage < 2000 ? 'speaking' : 'thinking';
    }
    return 'idle';
  };

  // Bull and Bear positions (opposing sides)
  const bullPos = { x: containerWidth * 0.25, y: containerHeight * 0.55 };
  const bearPos = { x: containerWidth * 0.75, y: containerHeight * 0.55 };

  // Observer positions (top row)
  const observerPositions = observerAgents.map((agent, index) => ({
    agent,
    x: containerWidth * (0.15 + index * 0.15),
    y: containerHeight * 0.15,
  }));

  // Get recent messages
  const getRecentMessages = (agentId: string, count: number = 2) => {
    return messages.filter(m => m.agent === agentId).slice(-count);
  };

  const bullMessages = getRecentMessages(bullAgent.id);
  const bearMessages = getRecentMessages(bearAgent.id);

  return (
    <Box
      sx={{
        position: 'relative',
        width: '100%',
        height: '100%',
        minHeight: 700,
      }}
    >
      {/* Chamber label */}
      <Box
        sx={{
          position: 'absolute',
          left: '50%',
          top: '35%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
        }}
      >
        <Typography
          variant="h5"
          sx={{
            color: 'text.secondary',
            fontWeight: 700,
            opacity: 0.5,
            fontSize: '3rem',
            letterSpacing: '0.1em',
          }}
        >
          🏛️
        </Typography>
        <Typography
          variant="caption"
          sx={{
            color: 'text.secondary',
            textTransform: 'uppercase',
            letterSpacing: '0.2em',
            fontWeight: 600,
          }}
        >
          Debate Chamber
        </Typography>
      </Box>

      {/* VS indicator */}
      <Box
        sx={{
          position: 'absolute',
          left: '50%',
          top: bullPos.y,
          transform: 'translate(-50%, -50%)',
          width: 60,
          height: 60,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.05)',
          border: '2px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backdropFilter: 'blur(10px)',
          zIndex: 1,
        }}
      >
        <Typography
          variant="h6"
          sx={{
            color: 'text.primary',
            fontWeight: 700,
          }}
        >
          VS
        </Typography>
      </Box>

      {/* Connection line between Bull and Bear */}
      {activeAgents.includes(bullAgent.id) && activeAgents.includes(bearAgent.id) && (
        <ConnectionLine
          from={bullPos}
          to={bearPos}
          color="#ef4444"
          animated
        />
      )}

      {/* Observer agents (gallery) */}
      <Box
        sx={{
          position: 'absolute',
          top: 20,
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: 2,
          padding: 2,
          background: 'rgba(255, 255, 255, 0.03)',
          borderRadius: 3,
          border: '1px solid rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(10px)',
        }}
      >
        <Typography
          variant="caption"
          sx={{
            alignSelf: 'center',
            color: 'text.secondary',
            mr: 1,
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            fontWeight: 600,
          }}
        >
          Gallery
        </Typography>
        {observerPositions.map(({ agent }) => (
          <AgentAvatar
            key={agent.id}
            name={agent.name}
            color={agent.color}
            status={getAgentStatus(agent.id)}
            size="small"
            showLabel={false}
            onClick={() => onAgentClick?.(agent)}
          />
        ))}
      </Box>

      {/* Bull Agent (left side) */}
      <Box
        sx={{
          position: 'absolute',
          left: bullPos.x,
          top: bullPos.y,
          transform: 'translate(-50%, -50%)',
          zIndex: 10,
        }}
      >
        <Box sx={{ textAlign: 'center' }}>
          <Typography
            variant="caption"
            sx={{
              color: bullAgent.color,
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              display: 'block',
              mb: 1,
            }}
          >
            🟢 Bull
          </Typography>
          <AgentAvatar
            name={bullAgent.name}
            color={bullAgent.color}
            status={getAgentStatus(bullAgent.id)}
            size="large"
            showLabel
            onClick={() => onAgentClick?.(bullAgent)}
          />
        </Box>
      </Box>

      {/* Bear Agent (right side) */}
      <Box
        sx={{
          position: 'absolute',
          left: bearPos.x,
          top: bearPos.y,
          transform: 'translate(-50%, -50%)',
          zIndex: 10,
        }}
      >
        <Box sx={{ textAlign: 'center' }}>
          <Typography
            variant="caption"
            sx={{
              color: bearAgent.color,
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              display: 'block',
              mb: 1,
            }}
          >
            🔴 Bear
          </Typography>
          <AgentAvatar
            name={bearAgent.name}
            color={bearAgent.color}
            status={getAgentStatus(bearAgent.id)}
            size="large"
            showLabel
            onClick={() => onAgentClick?.(bearAgent)}
          />
        </Box>
      </Box>

      {/* Bull messages */}
      {bullMessages.map((message, index) => (
        <Box
          key={`bull-${message.timestamp}-${index}`}
          sx={{
            position: 'absolute',
            left: bullPos.x - 180,
            top: bullPos.y + 100 + index * 120,
            zIndex: 5,
          }}
        >
          <MessageBubble
            message={message}
            agentColor={bullAgent.color}
            agentName={bullAgent.name}
          />
        </Box>
      ))}

      {/* Bear messages */}
      {bearMessages.map((message, index) => (
        <Box
          key={`bear-${message.timestamp}-${index}`}
          sx={{
            position: 'absolute',
            left: bearPos.x - 140,
            top: bearPos.y + 100 + index * 120,
            zIndex: 5,
          }}
        >
          <MessageBubble
            message={message}
            agentColor={bearAgent.color}
            agentName={bearAgent.name}
          />
        </Box>
      ))}
    </Box>
  );
};

export default CourtroomLayout;

