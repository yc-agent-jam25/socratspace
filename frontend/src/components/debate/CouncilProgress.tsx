/**
 * Council Progress Component
 * Clean, simplified visualization that fits properly
 */

import React from 'react';
import { Box, Typography, Grid, LinearProgress, Avatar, Chip } from '@mui/material';
import { keyframes } from '@mui/system';
import type { Phase, Agent, AgentMessage } from '../../lib/types';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import PendingIcon from '@mui/icons-material/Pending';

interface CouncilProgressProps {
  phase: Phase;
  agents: Agent[];
  messages: AgentMessage[];
  activeAgents: string[];
}

const pulse = keyframes`
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
`;

const CouncilProgress: React.FC<CouncilProgressProps> = ({
  phase,
  agents,
  messages,
  activeAgents,
}) => {
  const getAgentProgress = (agentId: string) => {
    const agentMessages = messages.filter(m => m.agent === agentId);
    return agentMessages.length;
  };

  const getAgentStatus = (agentId: string): 'pending' | 'active' | 'complete' => {
    const hasMessages = messages.some(m => m.agent === agentId);
    const isActive = activeAgents.includes(agentId);
    
    if (hasMessages && !isActive) return 'complete';
    if (isActive) return 'active';
    return 'pending';
  };

  const getPhaseAgents = () => {
    switch (phase) {
      case 'research':
        return {
          title: '🔍 Research Phase',
          description: 'Specialized agents analyzing different aspects',
          agents: agents.filter(a =>
            ['market_researcher', 'founder_evaluator', 'product_critic', 'financial_analyst', 'risk_assessor'].includes(a.id)
          ),
        };
      case 'debate':
        return {
          title: '⚖️ Debate Phase',
          description: 'Bull and Bear agents presenting arguments',
          agents: agents.filter(a => ['bull_agent', 'bear_agent'].includes(a.id)),
        };
      case 'decision':
        return {
          title: '✅ Decision Phase',
          description: 'Lead Partner making final decision',
          agents: agents.filter(a => a.id === 'lead_partner'),
        };
      default:
        return {
          title: '🏛️ Council Deliberation',
          description: 'Preparing analysis...',
          agents: [],
        };
    }
  };

  const phaseInfo = getPhaseAgents();
  const totalAgents = phaseInfo.agents.length;
  const completedAgents = phaseInfo.agents.filter(a => getAgentStatus(a.id) === 'complete').length;
  const progress = totalAgents > 0 ? (completedAgents / totalAgents) * 100 : 0;

  return (
    <Box>
      {/* Phase Header */}
      <Box
        sx={{
          p: 3,
          borderRadius: 3,
          background: 'rgba(139, 92, 246, 0.1)',
          border: '1px solid rgba(139, 92, 246, 0.3)',
          mb: 3,
        }}
      >
        <Typography
          variant="h5"
          sx={{
            fontWeight: 700,
            mb: 1,
            background: 'linear-gradient(135deg, #ffffff 0%, #a78bfa 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          {phaseInfo.title}
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mb: 2 }}>
          {phaseInfo.description}
        </Typography>

        {/* Progress bar */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{
              flex: 1,
              height: 8,
              borderRadius: 4,
              background: 'rgba(255, 255, 255, 0.1)',
              '& .MuiLinearProgress-bar': {
                background: 'linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%)',
                borderRadius: 4,
              },
            }}
          />
          <Typography
            variant="caption"
            sx={{
              fontWeight: 700,
              color: '#a78bfa',
              minWidth: 50,
            }}
          >
            {completedAgents}/{totalAgents}
          </Typography>
        </Box>
      </Box>

      {/* Agent Grid */}
      <Grid container spacing={2}>
        {phaseInfo.agents.map(agent => {
          const status = getAgentStatus(agent.id);
          const messageCount = getAgentProgress(agent.id);
          const isActive = status === 'active';
          const isComplete = status === 'complete';

          return (
            <Grid item xs={12} sm={6} md={4} key={agent.id}>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 2,
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: `1px solid ${isActive ? agent.color + '60' : 'rgba(255, 255, 255, 0.05)'}`,
                  transition: 'all 0.3s ease',
                  animation: isActive ? `${pulse} 2s infinite` : 'none',
                  boxShadow: isActive ? `0 0 20px ${agent.color}30` : 'none',
                  '&:hover': {
                    background: 'rgba(255, 255, 255, 0.05)',
                    transform: 'translateY(-2px)',
                  },
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1.5 }}>
                  {/* Avatar */}
                  <Avatar
                    sx={{
                      width: 40,
                      height: 40,
                      bgcolor: agent.color,
                      fontWeight: 700,
                      fontSize: '0.875rem',
                    }}
                  >
                    {agent.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
                  </Avatar>

                  {/* Info */}
                  <Box sx={{ flex: 1, minWidth: 0 }}>
                    <Typography
                      variant="subtitle2"
                      sx={{
                        fontWeight: 700,
                        color: 'text.primary',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {agent.name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                      {isActive && (
                        <Box
                          sx={{
                            width: 6,
                            height: 6,
                            borderRadius: '50%',
                            background: '#10b981',
                            animation: `${pulse} 1s infinite`,
                          }}
                        />
                      )}
                      <Typography
                        variant="caption"
                        sx={{
                          color: isActive ? '#10b981' : isComplete ? '#60a5fa' : 'text.disabled',
                          fontWeight: 600,
                        }}
                      >
                        {isActive ? 'Analyzing...' : isComplete ? 'Complete' : 'Waiting'}
                      </Typography>
                    </Box>
                  </Box>

                  {/* Status icon */}
                  {isComplete ? (
                    <CheckCircleIcon sx={{ color: '#10b981', fontSize: 20 }} />
                  ) : isActive ? (
                    <PendingIcon sx={{ color: agent.color, fontSize: 20 }} />
                  ) : null}
                </Box>

                {/* Message count */}
                {messageCount > 0 && (
                  <Chip
                    label={`${messageCount} insight${messageCount !== 1 ? 's' : ''}`}
                    size="small"
                    sx={{
                      height: 24,
                      fontSize: '0.7rem',
                      background: `${agent.color}20`,
                      color: agent.color,
                      fontWeight: 600,
                      border: `1px solid ${agent.color}40`,
                    }}
                  />
                )}
              </Box>
            </Grid>
          );
        })}
      </Grid>

      {/* All Phases Overview (when completed) */}
      {phase === 'completed' && (
        <Box
          sx={{
            mt: 3,
            p: 3,
            borderRadius: 3,
            background: 'rgba(16, 185, 129, 0.1)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
          }}
        >
          <Typography variant="h6" sx={{ fontWeight: 700, color: '#10b981', mb: 1 }}>
            ✅ Analysis Complete
          </Typography>
          <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            All agents have completed their analysis. Review the final decision in the Decision tab.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default CouncilProgress;

