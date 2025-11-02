/**
 * AgentReasoningCard Component
 * Enhanced card showing agent's reasoning steps with glassmorphism
 */

import React, { useState } from 'react';
import { Box, Typography, Collapse, IconButton, Stepper, Step, StepLabel, StepContent, Chip } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import PendingIcon from '@mui/icons-material/Pending';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import type { Agent, AgentMessage } from '../../lib/types';

interface AgentReasoningCardProps {
  agent: Agent;
  messages: AgentMessage[];
  active: boolean;
  onClick?: () => void;
}

const AgentReasoningCard: React.FC<AgentReasoningCardProps> = ({
  agent,
  messages,
  active,
  onClick,
}) => {
  const [expanded, setExpanded] = useState(false);

  const getStatusIcon = () => {
    if (active) return <PlayArrowIcon sx={{ color: agent.color, animation: 'pulse 1s infinite' }} />;
    if (messages.length > 0) return <CheckCircleIcon sx={{ color: '#10b981' }} />;
    return <PendingIcon sx={{ color: 'text.disabled' }} />;
  };

  const getStatusText = () => {
    if (active) return 'Analyzing...';
    if (messages.length > 0) return 'Complete';
    return 'Pending';
  };

  return (
    <Box
      onClick={onClick}
      sx={{
        position: 'relative',
        background: `linear-gradient(135deg, ${agent.color}08 0%, rgba(255,255,255,0.04) 100%)`,
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        border: `1px solid ${active ? agent.color + '60' : 'rgba(255,255,255,0.08)'}`,
        borderRadius: 3,
        overflow: 'hidden',
        transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
        cursor: 'pointer',
        '&:hover': {
          transform: 'translateY(-6px)',
          borderColor: agent.color + '80',
          boxShadow: `0 12px 48px ${agent.color}30, 0 0 0 1px ${agent.color}40`,
          background: `linear-gradient(135deg, ${agent.color}12 0%, rgba(255,255,255,0.06) 100%)`,
        },
        ...(active && {
          boxShadow: `0 8px 32px ${agent.color}40, 0 0 0 1px ${agent.color}60`,
          animation: 'gentlePulse 3s ease-in-out infinite',
          '@keyframes gentlePulse': {
            '0%, 100%': {
              boxShadow: `0 8px 32px ${agent.color}40, 0 0 0 1px ${agent.color}60`,
            },
            '50%': {
              boxShadow: `0 12px 48px ${agent.color}60, 0 0 0 1px ${agent.color}80`,
            },
          },
        }),
      }}
    >
      {/* Shimmer effect for active agents */}
      {active && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: '-100%',
            width: '100%',
            height: '100%',
            background: `linear-gradient(90deg, transparent, ${agent.color}20, transparent)`,
            animation: 'shimmer 2s infinite',
            '@keyframes shimmer': {
              '0%': { left: '-100%' },
              '100%': { left: '100%' },
            },
          }}
        />
      )}

      {/* Header */}
      <Box sx={{ p: 2.5, pb: messages.length === 0 ? 2.5 : 1.5 }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 1.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flex: 1 }}>
            <Box
              sx={{
                width: 48,
                height: 48,
                borderRadius: '12px',
                background: `linear-gradient(135deg, ${agent.color} 0%, ${agent.color}CC 100%)`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.25rem',
                fontWeight: 700,
                color: 'white',
                boxShadow: `0 4px 12px ${agent.color}40`,
                flexShrink: 0,
              }}
            >
              {agent.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
            </Box>
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <Typography
                variant="h6"
                sx={{
                  fontSize: '1rem',
                  fontWeight: 700,
                  color: 'text.primary',
                  mb: 0.25,
                  letterSpacing: '-0.01em',
                }}
              >
                {agent.name}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {getStatusIcon()}
                <Typography
                  variant="caption"
                  sx={{
                    color: active ? agent.color : 'text.secondary',
                    fontWeight: 600,
                    fontSize: '0.75rem',
                  }}
                >
                  {getStatusText()}
                </Typography>
              </Box>
            </Box>
          </Box>

          {messages.length > 0 && (
            <IconButton
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                setExpanded(!expanded);
              }}
              sx={{
                transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.3s',
                color: agent.color,
              }}
            >
              <ExpandMoreIcon />
            </IconButton>
          )}
        </Box>

        {/* Message count badge */}
        {messages.length > 0 && (
          <Chip
            label={`${messages.length} ${messages.length === 1 ? 'insight' : 'insights'}`}
            size="small"
            sx={{
              background: `${agent.color}20`,
              color: agent.color,
              fontWeight: 600,
              fontSize: '0.7rem',
              height: 24,
              border: `1px solid ${agent.color}40`,
            }}
          />
        )}
      </Box>

      {/* Reasoning Steps */}
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <Box
          sx={{
            p: 2.5,
            pt: 1,
            borderTop: '1px solid rgba(255,255,255,0.05)',
            background: 'rgba(0,0,0,0.2)',
          }}
        >
          <Typography
            variant="caption"
            sx={{
              color: 'text.secondary',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              display: 'block',
              mb: 2,
            }}
          >
            Reasoning Process
          </Typography>
          <Stepper orientation="vertical" sx={{ '.MuiStepConnector-line': { borderColor: `${agent.color}30` } }}>
            {messages.map((message, index) => (
              <Step key={message.timestamp} active completed>
                <StepLabel
                  StepIconComponent={() => (
                    <Box
                      sx={{
                        width: 24,
                        height: 24,
                        borderRadius: '50%',
                        background: `${agent.color}30`,
                        border: `2px solid ${agent.color}`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '0.7rem',
                        fontWeight: 700,
                        color: agent.color,
                      }}
                    >
                      {index + 1}
                    </Box>
                  )}
                  sx={{
                    '.MuiStepLabel-label': {
                      color: 'text.secondary',
                      fontSize: '0.75rem',
                      fontWeight: 600,
                    },
                  }}
                >
                  {message.message_type || 'Analysis'}
                </StepLabel>
                <StepContent>
                  <Box
                    sx={{
                      color: 'text.primary',
                      mb: 1,
                      '& p': { margin: '0.5rem 0', lineHeight: 1.6, fontSize: '0.875rem' },
                      '& p:first-of-type': { marginTop: 0 },
                      '& p:last-of-type': { marginBottom: 0 },
                      '& ul, & ol': { margin: '0.5rem 0', paddingLeft: '1.5rem', fontSize: '0.875rem' },
                      '& li': { marginBottom: '0.25rem', lineHeight: 1.6 },
                      '& strong': { fontWeight: 600 },
                      '& code': {
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        padding: '2px 4px',
                        borderRadius: 0.5,
                        fontSize: '0.8125rem'
                      },
                      '& h1, & h2, & h3': {
                        fontSize: '0.875rem',
                        fontWeight: 600,
                        margin: '0.5rem 0',
                      },
                      '& table': {
                        borderCollapse: 'collapse',
                        width: '100%',
                        margin: '0.5rem 0',
                        fontSize: '0.8125rem'
                      },
                      '& th, & td': {
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        padding: '0.5rem',
                        textAlign: 'left'
                      },
                      '& th': {
                        backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        fontWeight: 600
                      }
                    }}
                  >
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.message}</ReactMarkdown>
                  </Box>
                  <Typography
                    variant="caption"
                    sx={{
                      color: 'text.disabled',
                      fontSize: '0.7rem',
                    }}
                  >
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </Typography>
                </StepContent>
              </Step>
            ))}
          </Stepper>
        </Box>
      </Collapse>
    </Box>
  );
};

export default AgentReasoningCard;

