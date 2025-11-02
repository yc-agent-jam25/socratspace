/**
 * Council Avatar Bar Component
 * Simple visual representation of all agents - shows who's in the room
 */

import React from 'react';
import { Box, Avatar, Tooltip, Chip, Typography } from '@mui/material';
import { keyframes } from '@mui/system';
import type { Agent, AgentMessage } from '../../lib/types';

interface CouncilAvatarBarProps {
  agents: Agent[];
  messages: AgentMessage[];
  activeAgents: string[];
}

const pulse = keyframes`
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 currentColor;
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 4px transparent;
  }
`;

const glow = keyframes`
  0%, 100% {
    box-shadow: 0 0 20px currentColor;
  }
  50% {
    box-shadow: 0 0 30px currentColor;
  }
`;

const CouncilAvatarBar: React.FC<CouncilAvatarBarProps> = ({
  agents,
  messages,
  activeAgents,
}) => {
  const getAgentStatus = (agentId: string): 'pending' | 'active' | 'complete' => {
    const hasMessages = messages.some(m => m.agent === agentId);
    const isActive = activeAgents.includes(agentId);
    
    if (hasMessages && !isActive) return 'complete';
    if (isActive) return 'active';
    return 'pending';
  };

  const getMessageCount = (agentId: string): number => {
    return messages.filter(m => m.agent === agentId).length;
  };

  return (
    <Box
      sx={{
        p: 3,
        borderRadius: 3,
        background: 'rgba(255, 255, 255, 0.02)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        mb: 3,
      }}
    >
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          <Typography variant="h6" sx={{ fontWeight: 700, color: 'text.primary' }}>
            🏛️ Council Chamber
          </Typography>
          <Chip
            label={`${agents.length} Agents`}
            size="small"
            sx={{
              background: 'rgba(139, 92, 246, 0.2)',
              color: '#a78bfa',
              fontWeight: 600,
              fontSize: '0.75rem',
            }}
          />
        </Box>

        {/* Active count */}
        {activeAgents.length > 0 && (
          <Chip
            label={`${activeAgents.length} Active`}
            size="small"
            sx={{
              background: 'rgba(16, 185, 129, 0.2)',
              color: '#10b981',
              fontWeight: 600,
              fontSize: '0.75rem',
            }}
          />
        )}
      </Box>

      {/* Avatar Row */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: { xs: 1, sm: 2 },
          flexWrap: 'wrap',
          justifyContent: 'center',
        }}
      >
        {agents.map((agent, index) => {
          const status = getAgentStatus(agent.id);
          const messageCount = getMessageCount(agent.id);
          const isActive = status === 'active';
          const isComplete = status === 'complete';

          return (
            <Tooltip
              key={agent.id}
              title={
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 700 }}>
                    {agent.name}
                  </Typography>
                  <Typography variant="caption" sx={{ display: 'block', mt: 0.5 }}>
                    {isActive && '🟢 Currently analyzing'}
                    {isComplete && `✅ Complete (${messageCount} insights)`}
                    {status === 'pending' && '⏳ Waiting'}
                  </Typography>
                </Box>
              }
              arrow
            >
              <Box
                sx={{
                  position: 'relative',
                  animation: 'fadeIn 0.5s ease-out',
                  animationDelay: `${index * 0.1}s`,
                  animationFillMode: 'backwards',
                }}
              >
                <Avatar
                  sx={{
                    width: { xs: 48, sm: 64 },
                    height: { xs: 48, sm: 64 },
                    bgcolor: agent.color,
                    fontWeight: 700,
                    fontSize: { xs: '0.875rem', sm: '1rem' },
                    opacity: status === 'pending' ? 0.4 : 1,
                    border: isActive ? `3px solid ${agent.color}` : `2px solid ${agent.color}40`,
                    transition: 'all 0.3s ease',
                    cursor: 'pointer',
                    animation: isActive ? `${pulse} 2s infinite` : 'none',
                    boxShadow: isActive ? `0 0 20px ${agent.color}60` : 'none',
                    '&:hover': {
                      transform: 'scale(1.1)',
                      boxShadow: `0 0 25px ${agent.color}80`,
                    },
                  }}
                >
                  {agent.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
                </Avatar>

                {/* Status indicator */}
                <Box
                  sx={{
                    position: 'absolute',
                    bottom: -4,
                    right: -4,
                    width: { xs: 16, sm: 20 },
                    height: { xs: 16, sm: 20 },
                    borderRadius: '50%',
                    background: isActive ? '#10b981' : isComplete ? '#3b82f6' : '#6b7280',
                    border: '2px solid #141420',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: { xs: '0.5rem', sm: '0.6rem' },
                    animation: isActive ? `${glow} 2s infinite` : 'none',
                  }}
                >
                  {isActive && '●'}
                  {isComplete && '✓'}
                  {status === 'pending' && '○'}
                </Box>

                {/* Message count badge */}
                {messageCount > 0 && (
                  <Box
                    sx={{
                      position: 'absolute',
                      top: -8,
                      right: -8,
                      minWidth: 20,
                      height: 20,
                      borderRadius: '10px',
                      background: agent.color,
                      color: 'white',
                      fontSize: '0.65rem',
                      fontWeight: 700,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      px: 0.5,
                      boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
                    }}
                  >
                    {messageCount}
                  </Box>
                )}
              </Box>
            </Tooltip>
          );
        })}
      </Box>

      {/* Legend */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 3,
          mt: 3,
          pt: 2,
          borderTop: '1px solid rgba(255, 255, 255, 0.05)',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Box
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              background: '#10b981',
            }}
          />
          <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.75rem' }}>
            Active
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Box
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              background: '#3b82f6',
            }}
          />
          <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.75rem' }}>
            Complete
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Box
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              background: '#6b7280',
            }}
          />
          <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.75rem' }}>
            Pending
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default CouncilAvatarBar;

