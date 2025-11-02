/**
 * Agent Card Component
 * Displays individual agent status and messages
 */

import React, { useState } from 'react';
import { Card, CardContent, Typography, Box, Chip, Tooltip } from '@mui/material';
import type { Agent, AgentMessage } from '../lib/types';

interface AgentCardProps {
  agent: Agent;
  messages: AgentMessage[];
  active: boolean;
  onClick?: () => void;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, messages, active, onClick }) => {
  const latestMessage = messages.length > 0 ? messages[messages.length - 1] : null;
  const [isHovered, setIsHovered] = useState(false);

  const truncateMessage = (message: string, maxLength: number = 200): string => {
    if (message.length <= maxLength) return message;
    return message.substring(0, maxLength) + '...';
  };

  return (
    <Card
      elevation={active ? 8 : 2}
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      sx={{
        borderLeft: `4px solid ${agent.color}`,
        transition: 'all 0.3s ease',
        opacity: active ? 1 : 0.7,
        transform: isHovered ? 'translateY(-4px)' : 'translateY(0)',
        cursor: onClick ? 'pointer' : 'default',
        height: '100%',
        minHeight: 180,
        display: 'flex',
        flexDirection: 'column',
        animation: active ? 'pulse 2s infinite' : 'none',
        '@keyframes pulse': {
          '0%, 100%': {
            boxShadow: `0 0 10px ${agent.color}40`
          },
          '50%': {
            boxShadow: `0 0 20px ${agent.color}80`
          }
        }
      }}
    >
      <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Tooltip title={`${agent.name} - ${messages.length} message(s)`} arrow>
            <Typography 
              variant="h6" 
              sx={{ 
                color: agent.color,
                fontWeight: 600,
                fontSize: '1rem'
              }}
            >
              {agent.name}
            </Typography>
          </Tooltip>
          {active && (
            <Chip 
              label="Active" 
              color="primary" 
              size="small"
              sx={{ 
                animation: 'fadeIn 0.3s ease-in',
                fontWeight: 600
              }}
            />
          )}
        </Box>

        {latestMessage ? (
          <Typography 
            variant="body2" 
            color="text.secondary"
            sx={{ 
              flexGrow: 1,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              lineHeight: 1.5
            }}
          >
            {truncateMessage(latestMessage.message)}
          </Typography>
        ) : (
          <Typography 
            variant="body2" 
            color="text.disabled"
            sx={{ 
              flexGrow: 1,
              fontStyle: 'italic'
            }}
          >
            Waiting to start...
          </Typography>
        )}

        {messages.length > 0 && (
          <Typography 
            variant="caption" 
            color="text.secondary"
            sx={{ 
              mt: 2, 
              display: 'block',
              fontWeight: 500
            }}
          >
            {messages.length} message{messages.length !== 1 ? 's' : ''}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default AgentCard;
