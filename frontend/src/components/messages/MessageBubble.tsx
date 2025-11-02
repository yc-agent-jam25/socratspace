/**
 * MessageBubble Component
 * Floating message card with animations
 */

import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { keyframes } from '@mui/system';
import type { AgentMessage } from '../../lib/types';

interface MessageBubbleProps {
  message: AgentMessage;
  agentColor: string;
  agentName: string;
  position?: { x: number; y: number };
  onClose?: () => void;
}

// Float animation
const floatAnimation = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
`;

// Fade in animation
const fadeInAnimation = keyframes`
  from {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
`;

const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  agentColor,
  agentName,
  position,
}) => {
  const formatTime = (timestamp: number): string => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Paper
      elevation={3}
      sx={{
        position: position ? 'absolute' : 'relative',
        left: position?.x || 'auto',
        top: position?.y || 'auto',
        maxWidth: 320,
        padding: 2,
        background: 'rgba(255, 255, 255, 0.08)',
        backdropFilter: 'blur(20px)',
        border: `1px solid ${agentColor}40`,
        borderLeft: `4px solid ${agentColor}`,
        borderRadius: 2,
        animation: `${fadeInAnimation} 0.4s ease-out, ${floatAnimation} 6s ease-in-out infinite`,
        boxShadow: `0 8px 32px rgba(0, 0, 0, 0.3), 0 0 20px ${agentColor}20`,
        cursor: 'default',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'scale(1.02)',
          boxShadow: `0 12px 48px rgba(0, 0, 0, 0.4), 0 0 30px ${agentColor}40`,
          borderColor: `${agentColor}60`,
        },
      }}
    >
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Typography
          variant="caption"
          sx={{
            color: agentColor,
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
          }}
        >
          {agentName}
        </Typography>
        <Typography
          variant="caption"
          sx={{
            color: 'text.secondary',
            fontSize: '0.7rem',
          }}
        >
          {formatTime(message.timestamp)}
        </Typography>
      </Box>

      {/* Message content */}
      <Typography
        variant="body2"
        sx={{
          color: 'text.primary',
          lineHeight: 1.6,
          wordWrap: 'break-word',
        }}
      >
        {message.message}
      </Typography>

      {/* Type indicator */}
      {message.message_type && (
        <Box
          sx={{
            mt: 1,
            pt: 1,
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          }}
        >
          <Typography
            variant="caption"
            sx={{
              color: 'text.secondary',
              fontSize: '0.7rem',
              fontStyle: 'italic',
            }}
          >
            {message.message_type}
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default MessageBubble;

