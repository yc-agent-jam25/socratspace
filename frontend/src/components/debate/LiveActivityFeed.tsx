/**
 * Live Activity Feed Component
 * Real-time message stream with agent avatars - no popups or expanding
 */

import React, { useEffect, useRef, useState } from 'react';
import {
  Box,
  Typography,
  Stack,
  Avatar,
  Chip,
  TextField,
  InputAdornment,
  IconButton,
  Modal,
  Fade,
  Backdrop,
} from '@mui/material';
import { keyframes } from '@mui/system';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { AgentMessage, Agent } from '../../lib/types';
import { preprocessMarkdown } from '../../lib/markdownUtils';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import FilterListIcon from '@mui/icons-material/FilterList';
import FullscreenIcon from '@mui/icons-material/Fullscreen';
import FullscreenExitIcon from '@mui/icons-material/FullscreenExit';

interface LiveActivityFeedProps {
  messages: AgentMessage[];
  agents: Agent[];
  activeAgents: string[];
}

const slideIn = keyframes`
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
`;

const pulse = keyframes`
  0%, 100% {
    box-shadow: 0 0 0 0 currentColor;
  }
  50% {
    box-shadow: 0 0 0 4px transparent;
  }
`;


const LiveActivityFeed: React.FC<LiveActivityFeedProps> = ({
  messages,
  agents,
  activeAgents,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [fullscreen, setFullscreen] = useState(false);
  const feedRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (autoScroll && feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [messages, autoScroll]);

  // Check if user has scrolled up
  const handleScroll = () => {
    if (feedRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = feedRef.current;
      const isAtBottom = scrollHeight - scrollTop - clientHeight < 50;
      setAutoScroll(isAtBottom);
    }
  };

  const getAgent = (agentId: string): Agent | undefined => {
    // message.agent is normalized to an ID by useSSE hook (e.g., 'market_researcher')
    // Find agent by ID
    return agents.find(a => a.id === agentId);
  };

  const isAgentActive = (agentId: string): boolean => {
    return activeAgents.includes(agentId);
  };

  // Filter messages
  const filteredMessages = messages.filter(message => {
    // Search filter - message.agent is an ID, so find agent to get name for search
    const agent = getAgent(message.agent);
    const agentName = agent?.name || message.agent; // Fallback to ID if agent not found
    const matchesSearch = searchQuery === '' || 
      message.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agentName.toLowerCase().includes(searchQuery.toLowerCase());
    
    // Agent filter
    // Both message.agent and selectedAgent are IDs
    const matchesAgent = selectedAgent === null || message.agent === selectedAgent;
    
    return matchesSearch && matchesAgent;
  });

  // Group messages by phase
  const messagesByPhase = filteredMessages.reduce((acc, message) => {
    const timestamp = message.timestamp;
    const phase = timestamp < messages[Math.floor(messages.length / 3)]?.timestamp 
      ? 'Research Phase'
      : timestamp < messages[Math.floor(messages.length * 2 / 3)]?.timestamp
      ? 'Debate Phase'
      : 'Decision Phase';
    
    if (!acc[phase]) acc[phase] = [];
    acc[phase].push(message);
    return acc;
  }, {} as Record<string, AgentMessage[]>);

  return (
    <>
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'row',
      }}
    >
      {/* Left sidebar - Filters */}
      <Box
        sx={{
          width: 260,
          flexShrink: 0,
          borderRight: '1px solid rgba(255, 255, 255, 0.08)',
          background: 'rgba(255, 255, 255, 0.02)',
          display: 'flex',
          flexDirection: 'column',
          overflowY: 'auto',
        }}
      >
        <Box sx={{ p: 1 }}>
          {/* Search */}
          <TextField
            size="small"
            fullWidth
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ fontSize: 18, color: 'text.secondary' }} />
                </InputAdornment>
              ),
              endAdornment: searchQuery && (
                <InputAdornment position="end">
                  <IconButton size="small" onClick={() => setSearchQuery('')}>
                    <ClearIcon sx={{ fontSize: 16 }} />
                  </IconButton>
                </InputAdornment>
              ),
            }}
            sx={{
              mb: 1.5,
              '& .MuiOutlinedInput-root': {
                background: 'rgba(0, 0, 0, 0.2)',
                height: 36,
                fontSize: '0.875rem',
              },
            }}
          />

          {/* Agent filters header */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.75, mb: 1 }}>
            <FilterListIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
            <Typography variant="caption" sx={{ fontWeight: 700, color: 'text.secondary', textTransform: 'uppercase', letterSpacing: '0.05em', fontSize: '0.7rem' }}>
              Agents
            </Typography>
          </Box>

          {/* Agent filter chips - compact vertical list */}
          <Stack spacing={0.5} sx={{ mb: 1.5 }}>
            <Box
              onClick={() => setSelectedAgent(null)}
              sx={{
                width: '100%',
                height: 36,
                px: 1.25,
                py: 0.75,
                display: 'flex',
                alignItems: 'center',
                borderRadius: 1.5,
                background: selectedAgent === null ? '#8b5cf6' : 'rgba(255, 255, 255, 0.05)',
                color: selectedAgent === null ? 'white' : 'text.secondary',
                fontWeight: 600,
                fontSize: '0.875rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                '&:hover': {
                  background: selectedAgent === null ? '#7c3aed' : 'rgba(255, 255, 255, 0.1)',
                  transform: 'translateX(2px)',
                },
              }}
            >
              <Typography
                variant="body2"
                sx={{
                  width: '100%',
                  fontWeight: 600,
                  fontSize: '0.875rem',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                }}
              >
                All Agents
              </Typography>
            </Box>
            {agents.map(agent => (
              <Box
                key={agent.id}
                onClick={() => setSelectedAgent(agent.id === selectedAgent ? null : agent.id)}
                sx={{
                  width: '100%',
                  height: 36,
                  px: 1.25,
                  py: 0.75,
                  display: 'flex',
                  alignItems: 'center',
                  borderRadius: 1.5,
                  background: selectedAgent === agent.id ? agent.color : 'rgba(0, 0, 0, 0.2)',
                  color: selectedAgent === agent.id ? 'white' : 'text.secondary',
                  fontWeight: 600,
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                  border: selectedAgent === agent.id ? 'none' : `1px solid ${agent.color}40`,
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    background: selectedAgent === agent.id ? agent.color : `${agent.color}30`,
                    color: selectedAgent === agent.id ? 'white' : agent.color,
                    transform: 'translateX(2px)',
                    borderColor: selectedAgent === agent.id ? 'none' : agent.color,
                  },
                }}
              >
                <Typography
                  variant="body2"
                  sx={{
                    width: '100%',
                    fontWeight: 600,
                    fontSize: '0.875rem',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                  }}
                >
                  {agent.name}
                </Typography>
              </Box>
            ))}
          </Stack>

          {/* Message count */}
          <Box
            sx={{
              p: 1,
              borderRadius: 1,
              background: 'rgba(139, 92, 246, 0.15)',
              border: '1px solid rgba(139, 92, 246, 0.3)',
            }}
          >
            <Typography
              variant="caption"
              sx={{
                display: 'block',
                textAlign: 'center',
                color: '#a78bfa',
                fontWeight: 700,
                fontSize: '0.75rem',
              }}
            >
              {filteredMessages.length} message{filteredMessages.length !== 1 ? 's' : ''}
            </Typography>
          </Box>
        </Box>
      </Box>

      {/* Right side - Message feed */}
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* Header */}
        <Box
          sx={{
            p: 2,
            borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
            background: 'rgba(255, 255, 255, 0.02)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <Typography variant="h6" sx={{ fontWeight: 700 }}>
            Live Activity Feed
          </Typography>
          <IconButton
            onClick={() => setFullscreen(true)}
            sx={{
              color: 'rgba(139, 92, 246, 0.8)',
              '&:hover': {
                color: '#8b5cf6',
                background: 'rgba(139, 92, 246, 0.1)',
              },
            }}
          >
            <FullscreenIcon />
          </IconButton>
        </Box>

        {/* Message feed */}
        <Box
          ref={feedRef}
          onScroll={handleScroll}
          sx={{
            flex: 1,
            overflowY: 'auto',
            overflowX: 'hidden', // Prevent horizontal scroll
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            position: 'relative', // For absolute positioned auto-scroll indicator
          }}
        >
        {Object.entries(messagesByPhase).map(([phase, phaseMessages]) => (
          <Box key={phase}>
            {/* Phase divider */}
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 2,
                mb: 2,
                mt: 2,
              }}
            >
              <Box
                sx={{
                  flex: 1,
                  height: 1,
                  background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent)',
                }}
              />
              <Chip
                label={phase}
                size="small"
                sx={{
                  background: 'rgba(59, 130, 246, 0.2)',
                  color: '#60a5fa',
                  fontWeight: 700,
                  fontSize: '0.75rem',
                  letterSpacing: '0.05em',
                }}
              />
              <Box
                sx={{
                  flex: 1,
                  height: 1,
                  background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent)',
                }}
              />
            </Box>

            {/* Messages in this phase */}
            {phaseMessages.map((message, index) => {
              const agent = getAgent(message.agent);
              if (!agent) return null;

              const isActive = isAgentActive(agent.id);

              return (
                <Box
                  key={`${message.agent}-${message.timestamp}-${index}`}
                  sx={{
                    display: 'flex',
                    gap: 2,
                    mb: 2,
                    animation: `${slideIn} 0.3s ease-out`,
                    '&:hover': {
                      '& .message-card': {
                        background: 'rgba(255, 255, 255, 0.06)',
                        borderColor: `${agent.color}60`,
                      },
                    },
                  }}
                >
                  {/* Agent avatar */}
                  <Box sx={{ position: 'relative', flexShrink: 0 }}>
                    <Avatar
                      sx={{
                        width: 40,
                        height: 40,
                        bgcolor: agent.color,
                        fontWeight: 700,
                        fontSize: '0.875rem',
                        border: isActive ? `2px solid ${agent.color}` : 'none',
                        animation: isActive ? `${pulse} 2s infinite` : 'none',
                      }}
                    >
                      {agent.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
                    </Avatar>
                    {isActive && (
                      <Box
                        sx={{
                          position: 'absolute',
                          bottom: -2,
                          right: -2,
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          background: '#10b981',
                          border: '2px solid #141420',
                        }}
                      />
                    )}
                  </Box>

                  {/* Message content */}
                  <Box sx={{ flex: 1, minWidth: 0 }}>
                    <Box
                      className="message-card"
                      sx={{
                        p: 2,
                        borderRadius: 2,
                        background: 'rgba(255, 255, 255, 0.03)',
                        border: `1px solid rgba(255, 255, 255, 0.05)`,
                        borderLeft: `3px solid ${agent.color}`,
                        transition: 'all 0.2s ease',
                      }}
                    >
                      {/* Header */}
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontWeight: 700,
                            color: agent.color,
                          }}
                        >
                          {agent.name}
                        </Typography>
                        {message.message_type && (
                          <Chip
                            label={message.message_type}
                            size="small"
                            sx={{
                              height: 20,
                              fontSize: '0.65rem',
                              background: `${agent.color}20`,
                              color: agent.color,
                              fontWeight: 600,
                            }}
                          />
                        )}
                        <Typography
                          variant="caption"
                          sx={{
                            ml: 'auto',
                            color: 'text.disabled',
                            fontSize: '0.7rem',
                          }}
                        >
                          {new Date(message.timestamp).toLocaleTimeString()}
                        </Typography>
                      </Box>

                      {/* Message text */}
                      <Box
                        sx={{
                          color: 'text.primary',
                          '& p': { margin: '0.5rem 0', lineHeight: 1.6, fontSize: '0.875rem' },
                          '& p:first-of-type': { marginTop: 0 },
                          '& p:last-of-type': { marginBottom: 0 },
                          '& ul, & ol': { margin: '0.5rem 0', paddingLeft: '1.5rem' },
                          '& li': { marginBottom: '0.25rem', lineHeight: 1.6 },
                          '& strong': { fontWeight: 600 },
                          '& em': { fontStyle: 'italic' },
                          '& code': {
                            backgroundColor: 'rgba(255, 255, 255, 0.1)',
                            padding: '2px 6px',
                            borderRadius: 1,
                            fontSize: '0.8125rem',
                            fontFamily: 'monospace'
                          },
                          '& pre': {
                            backgroundColor: 'rgba(255, 255, 255, 0.05)',
                            padding: '1rem',
                            borderRadius: 1,
                            overflow: 'auto',
                            margin: '0.5rem 0'
                          },
                          '& h1, & h2, & h3, & h4, & h5, & h6': {
                            fontWeight: 600,
                            margin: '0.75rem 0 0.5rem 0',
                            lineHeight: 1.4
                          },
                          '& h1': { fontSize: '1.25rem' },
                          '& h2': { fontSize: '1.1rem' },
                          '& h3': { fontSize: '1rem' },
                          '& h4, & h5, & h6': { fontSize: '0.875rem' },
                          '& blockquote': {
                            borderLeft: '4px solid',
                            borderColor: agent.color,
                            paddingLeft: '1rem',
                            margin: '0.5rem 0',
                            fontStyle: 'italic',
                            opacity: 0.8
                          },
                          '& > *': {
                            overflowX: 'auto',
                            overflowY: 'visible',
                          },
                          '& table': {
                            borderCollapse: 'collapse',
                            width: '100%',
                            margin: '0.5rem 0',
                            fontSize: '0.8125rem',
                            display: 'table',
                            minWidth: '100%',
                          },
                          '& th, & td': {
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            padding: '0.5rem',
                            textAlign: 'left',
                            whiteSpace: 'normal',
                            wordWrap: 'break-word',
                          },
                          '& th': {
                            backgroundColor: 'rgba(255, 255, 255, 0.05)',
                            fontWeight: 600
                          }
                        }}
                      >
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{preprocessMarkdown(message.message)}</ReactMarkdown>
                      </Box>
                    </Box>
                  </Box>
                </Box>
              );
            })}
          </Box>
        ))}

        {filteredMessages.length === 0 && (
          <Box
            sx={{
              textAlign: 'center',
              py: 8,
            }}
          >
            <Typography variant="body1" color="text.secondary">
              {searchQuery || selectedAgent
                ? 'No messages match your filters'
                : 'Waiting for agents to start analysis...'}
            </Typography>
          </Box>
        )}
      </Box>

        {/* Auto-scroll indicator */}
        {!autoScroll && (
          <Box
            sx={{
              position: 'absolute',
              bottom: 80,
              left: '50%',
              transform: 'translateX(-50%)',
              zIndex: 10,
            }}
          >
            <Chip
              label="New messages below"
              size="small"
              onClick={() => {
                setAutoScroll(true);
                if (feedRef.current) {
                  feedRef.current.scrollTop = feedRef.current.scrollHeight;
                }
              }}
              sx={{
                background: '#8b5cf6',
                color: 'white',
                fontWeight: 600,
                cursor: 'pointer',
                boxShadow: '0 4px 12px rgba(139, 92, 246, 0.4)',
                '&:hover': {
                  background: '#7c3aed',
                },
              }}
            />
          </Box>
        )}
      </Box>
    </Box>

    {/* Fullscreen Modal */}
    <Modal
      open={fullscreen}
      onClose={() => setFullscreen(false)}
      closeAfterTransition
      slots={{ backdrop: Backdrop }}
      slotProps={{
        backdrop: {
          timeout: 500,
          sx: { backgroundColor: 'rgba(0, 0, 0, 0.95)' },
        },
      }}
    >
      <Fade in={fullscreen}>
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            flexDirection: 'column',
            bgcolor: 'rgba(10, 10, 20, 0.98)',
            backdropFilter: 'blur(20px)',
            overflow: 'hidden',
          }}
        >
          {/* Fullscreen Header */}
          <Box
            sx={{
              p: 3,
              borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
              background: 'rgba(139, 92, 246, 0.05)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>
                Live Activity Feed
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Full document view • {filteredMessages.length} messages
              </Typography>
            </Box>
            <IconButton
              onClick={() => setFullscreen(false)}
              sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                '&:hover': {
                  color: 'white',
                  background: 'rgba(255, 255, 255, 0.1)',
                },
              }}
            >
              <FullscreenExitIcon />
            </IconButton>
          </Box>

          {/* Fullscreen Content */}
          <Box
            sx={{
              flex: 1,
              overflowY: 'auto',
              overflowX: 'hidden',
              px: 6,
              py: 4,
              maxWidth: 1200,
              mx: 'auto',
              width: '100%',
            }}
          >
            {/* Search in fullscreen */}
            <Box sx={{ mb: 4 }}>
              <TextField
                size="medium"
                fullWidth
                placeholder="Search messages..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                  endAdornment: searchQuery && (
                    <InputAdornment position="end">
                      <IconButton size="small" onClick={() => setSearchQuery('')}>
                        <ClearIcon />
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    background: 'rgba(0, 0, 0, 0.3)',
                    '&:hover': {
                      background: 'rgba(0, 0, 0, 0.4)',
                    },
                  },
                }}
              />
            </Box>

            {/* Render all filtered messages */}
            {filteredMessages.length === 0 ? (
              <Box
                sx={{
                  textAlign: 'center',
                  py: 12,
                  px: 4,
                }}
              >
                <Typography variant="h5" sx={{ mb: 2, color: 'text.secondary' }}>
                  {searchQuery || selectedAgent
                    ? 'No messages match your filters'
                    : 'No messages yet'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {searchQuery || selectedAgent
                    ? 'Try adjusting your search or filter settings'
                    : 'Messages will appear here as agents start their analysis'}
                </Typography>
              </Box>
            ) : (
              <Stack spacing={3}>
                {filteredMessages.map((message, index) => {
                  const agent = getAgent(message.agent);
                  if (!agent) {
                    // Skip messages from unknown agents
                    return null;
                  }

                return (
                  <Box
                    key={`fullscreen-${message.agent}-${message.timestamp}-${index}`}
                    sx={{
                      animation: `${slideIn} 0.3s ease-out`,
                      p: 3,
                      borderRadius: 2,
                      background: 'rgba(255, 255, 255, 0.03)',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      '&:hover': {
                        background: 'rgba(255, 255, 255, 0.05)',
                        borderColor: `${agent.color}40`,
                      },
                      transition: 'all 0.2s ease',
                    }}
                  >
                    {/* Agent info */}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                      <Avatar
                        sx={{
                          width: 44,
                          height: 44,
                          bgcolor: agent.color,
                          border: `2px solid ${agent.color}40`,
                          fontSize: '1.2rem',
                        }}
                      >
                        {agent.name.charAt(0)}
                      </Avatar>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 700, color: agent.color }}>
                          {agent.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(message.timestamp).toLocaleTimeString()} • {message.message_type}
                        </Typography>
                      </Box>
                    </Box>

                    {/* Message content */}
                    <Box
                      sx={{
                        fontSize: '0.95rem',
                        lineHeight: 1.7,
                        color: 'rgba(255, 255, 255, 0.9)',
                        '& > *': {
                          overflowX: 'auto',
                          overflowY: 'visible',
                        },
                        '& p': {
                          mb: 1.5,
                        },
                        '& ul, & ol': {
                          ml: 2,
                          mb: 1.5,
                        },
                        '& li': {
                          mb: 0.5,
                        },
                        '& code': {
                          background: 'rgba(139, 92, 246, 0.15)',
                          padding: '0.2em 0.4em',
                          borderRadius: '4px',
                          fontSize: '0.9em',
                          fontFamily: 'monospace',
                        },
                        '& pre': {
                          background: 'rgba(0, 0, 0, 0.4)',
                          padding: 2,
                          borderRadius: 1,
                          overflow: 'auto',
                          mb: 1.5,
                        },
                        '& table': {
                          borderCollapse: 'collapse',
                          width: '100%',
                          margin: '1rem 0',
                          fontSize: '0.875rem',
                          display: 'table',
                          minWidth: '100%',
                        },
                        '& th, & td': {
                          border: '1px solid rgba(255, 255, 255, 0.1)',
                          padding: '0.75rem',
                          textAlign: 'left',
                          whiteSpace: 'normal',
                          wordWrap: 'break-word',
                        },
                        '& th': {
                          background: 'rgba(139, 92, 246, 0.2)',
                          fontWeight: 700,
                          color: '#a78bfa',
                        },
                        '& td': {
                          background: 'rgba(0, 0, 0, 0.2)',
                        },
                        '& tr:hover td': {
                          background: 'rgba(139, 92, 246, 0.1)',
                        },
                        '& blockquote': {
                          borderLeft: `4px solid ${agent.color}`,
                          pl: 2,
                          ml: 0,
                          mb: 1.5,
                          fontStyle: 'italic',
                          color: 'rgba(255, 255, 255, 0.7)',
                        },
                        '& h1, & h2, & h3, & h4': {
                          mt: 2,
                          mb: 1,
                          fontWeight: 700,
                          color: agent.color,
                        },
                      }}
                    >
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{preprocessMarkdown(message.message)}</ReactMarkdown>
                    </Box>
                  </Box>
                );
              })}
              </Stack>
            )}
          </Box>
        </Box>
      </Fade>
    </Modal>
    </>
  );
};

export default LiveActivityFeed;

