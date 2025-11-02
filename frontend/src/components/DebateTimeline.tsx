/**
 * Debate Timeline Component
 * Visual timeline of agent activities during debate
 */

import React from 'react';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  TimelineOppositeContent
} from '@mui/lab';
import { Paper, Typography, Box } from '@mui/material';
import type { AgentMessage } from '../lib/types';

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

      <Timeline position="right">
        {messages.map((message, index) => (
          <TimelineItem key={index}>
            <TimelineOppositeContent
              sx={{ m: 'auto 0' }}
              variant="body2"
              color="text.secondary"
            >
              {formatTime(message.timestamp)}
            </TimelineOppositeContent>

            <TimelineSeparator>
              <TimelineDot
                sx={{
                  bgcolor: agentColors[message.agent] || 'grey.500'
                }}
              />
              {index < messages.length - 1 && <TimelineConnector />}
            </TimelineSeparator>

            <TimelineContent sx={{ py: '12px', px: 2 }}>
              <Box>
                <Typography 
                  variant="subtitle2" 
                  sx={{ 
                    fontWeight: 600,
                    color: agentColors[message.agent] || 'text.primary'
                  }}
                >
                  {getAgentName(message.agent)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {message.message.substring(0, 100)}
                  {message.message.length > 100 && '...'}
                </Typography>
              </Box>
            </TimelineContent>
          </TimelineItem>
        ))}
      </Timeline>

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

