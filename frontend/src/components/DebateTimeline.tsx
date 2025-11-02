/**
 * Debate Timeline Component
 * Visual timeline of agent activities during debate
 */

import React from 'react';
import { Paper, Typography, Box } from '@mui/material';
import type { AgentMessage } from '../lib/types';

// Timeline components (simplified - @mui/lab Timeline is optional)
// Using custom timeline instead

interface DebateTimelineProps {
  messages: AgentMessage[];
  agentColors: Record<string, string>;
}

const DebateTimeline: React.FC<DebateTimelineProps> = ({ messages, agentColors }) => {
  const formatTime = (timestamp: number): string => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getAgentName = (agentId: string): string => {
    const names: Record<string, string> = {
      market_researcher: 'Market Researcher',
      founder_evaluator: 'Founder Evaluator',
      product_critic: 'Product Critic',
      financial_analyst: 'Financial Analyst',
      risk_assessor: 'Risk Assessor',
      bull_agent: 'Bull Agent',
      bear_agent: 'Bear Agent',
      lead_partner: 'Lead Partner'
    };
    return names[agentId] || agentId;
  };

  return (
    <Paper elevation={2} sx={{ p: 3, maxHeight: 600, overflow: 'auto' }}>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
        Debate Timeline
      </Typography>

      <Box>
        {messages.map((message, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              gap: 2,
              mb: 3,
              position: 'relative',
              pl: 4,
              '&::before': {
                content: '""',
                position: 'absolute',
                left: 8,
                top: 0,
                bottom: index === messages.length - 1 ? '50%' : '-24px',
                width: 2,
                bgcolor: agentColors[message.agent] || 'grey.500',
                opacity: 0.5,
              },
              '&::after': {
                content: '""',
                position: 'absolute',
                left: 6,
                top: 8,
                width: 12,
                height: 12,
                borderRadius: '50%',
                bgcolor: agentColors[message.agent] || 'grey.500',
                border: '2px solid',
                borderColor: 'background.paper',
              },
            }}
          >
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                <Typography
                  variant="subtitle2"
                  sx={{
                    fontWeight: 600,
                    color: agentColors[message.agent] || 'text.primary',
                  }}
                >
                  {getAgentName(message.agent)}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                  {formatTime(message.timestamp)}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                {message.message.substring(0, 100)}
                {message.message.length > 100 && '...'}
              </Typography>
            </Box>
          </Box>
        ))}
      </Box>

      {messages.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="body2" color="text.secondary">
            No timeline events yet
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default DebateTimeline;

