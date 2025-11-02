/**
 * SummitLayout Component
 * Decision phase layout with Lead Partner centered
 */

import React from 'react';
import { Box, Typography, Grid } from '@mui/material';
import type { Agent, AgentMessage } from '../../lib/types';
import AgentAvatar from '../agents/AgentAvatar';
import MessageBubble from '../messages/MessageBubble';
import GlassCard from '../shared/GlassCard';

interface SummitLayoutProps {
  leadPartner: Agent;
  researchAgents: Agent[];
  messages: AgentMessage[];
  activeAgents: string[];
  onAgentClick?: (agent: Agent) => void;
  containerWidth: number;
  containerHeight: number;
}

const SummitLayout: React.FC<SummitLayoutProps> = ({
  leadPartner,
  researchAgents,
  messages,
  activeAgents,
  onAgentClick,
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

  // Get lead partner messages
  const leadMessages = messages
    .filter(m => m.agent === leadPartner.id)
    .slice(-2);

  // Get evidence cards (research findings)
  const evidenceMessages = messages
    .filter(m => m.message_type === 'analysis' || m.message_type === 'insight')
    .slice(0, 6); // Show max 6 evidence cards

  return (
    <Box
      sx={{
        position: 'relative',
        width: '100%',
        height: '100%',
        minHeight: containerHeight || 700,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        pt: 4,
      }}
    >
      {/* Title */}
      <Typography
        variant="h4"
        sx={{
          color: 'text.primary',
          fontWeight: 700,
          mb: 1,
          textAlign: 'center',
          letterSpacing: '0.05em',
        }}
      >
        Final Deliberation
      </Typography>
      <Typography
        variant="body2"
        sx={{
          color: 'text.secondary',
          mb: 4,
          textAlign: 'center',
        }}
      >
        Lead Partner reviewing all evidence
      </Typography>

      {/* Lead Partner (centered and prominent) */}
      <Box
        sx={{
          position: 'relative',
          zIndex: 10,
          mb: 4,
        }}
      >
        <AgentAvatar
          name={leadPartner.name}
          color={leadPartner.color}
          status={getAgentStatus(leadPartner.id)}
          size="large"
          showLabel
          onClick={() => onAgentClick?.(leadPartner)}
        />
      </Box>

      {/* Lead Partner messages */}
      {leadMessages.length > 0 && (
        <Box sx={{ mb: 4, maxWidth: 600 }}>
          {leadMessages.map((message, index) => (
            <Box key={`lead-${message.timestamp}-${index}`} sx={{ mb: 2 }}>
              <MessageBubble
                message={message}
                agentColor={leadPartner.color}
                agentName={leadPartner.name}
              />
            </Box>
          ))}
        </Box>
      )}

      {/* Evidence Grid */}
      {evidenceMessages.length > 0 && (
        <Box sx={{ width: '100%', maxWidth: 1200, px: 2 }}>
          <Typography
            variant="h6"
            sx={{
              color: 'text.secondary',
              fontWeight: 600,
              mb: 3,
              textAlign: 'center',
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              fontSize: '0.875rem',
            }}
          >
            Evidence Under Review
          </Typography>
          <Grid container spacing={2}>
            {evidenceMessages.map((message, index) => {
              const agent = researchAgents.find(a => a.id === message.agent);
              if (!agent) return null;

              return (
                <Grid item xs={12} sm={6} md={4} key={`evidence-${message.timestamp}-${index}`}>
                  <GlassCard
                    intensity="medium"
                    sx={{
                      height: '100%',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease',
                      borderLeft: `3px solid ${agent.color}`,
                      '&:hover': {
                        transform: 'translateY(-4px)',
                        borderColor: agent.color,
                      },
                    }}
                  >
                    <Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        <Box
                          sx={{
                            width: 32,
                            height: 32,
                            borderRadius: '50%',
                            bgcolor: agent.color,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '0.75rem',
                            fontWeight: 600,
                          }}
                        >
                          {agent.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
                        </Box>
                        <Box>
                          <Typography
                            variant="caption"
                            sx={{
                              color: agent.color,
                              fontWeight: 600,
                              display: 'block',
                            }}
                          >
                            {agent.name}
                          </Typography>
                          <Typography
                            variant="caption"
                            sx={{
                              color: 'text.secondary',
                              fontSize: '0.7rem',
                            }}
                          >
                            {message.message_type}
                          </Typography>
                        </Box>
                      </Box>
                      <Typography
                        variant="body2"
                        sx={{
                          color: 'text.primary',
                          lineHeight: 1.5,
                          display: '-webkit-box',
                          WebkitLineClamp: 4,
                          WebkitBoxOrient: 'vertical',
                          overflow: 'hidden',
                        }}
                      >
                        {message.message}
                      </Typography>
                    </Box>
                  </GlassCard>
                </Grid>
              );
            })}
          </Grid>
        </Box>
      )}

      {/* Research agents footer (small avatars) */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 20,
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: 1,
          padding: 1.5,
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
            fontSize: '0.7rem',
          }}
        >
          Submitted by:
        </Typography>
        {researchAgents.map(agent => (
          <AgentAvatar
            key={agent.id}
            name={agent.name}
            color={agent.color}
            status="done"
            size="small"
            showLabel={false}
            onClick={() => onAgentClick?.(agent)}
          />
        ))}
      </Box>
    </Box>
  );
};

export default SummitLayout;

