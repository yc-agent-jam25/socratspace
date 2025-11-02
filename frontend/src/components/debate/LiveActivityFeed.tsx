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
  Tooltip,
} from '@mui/material';
import { keyframes } from '@mui/system';
import type { AgentMessage, Agent } from '../../lib/types';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import FilterListIcon from '@mui/icons-material/FilterList';

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
    // Agent names are already normalized in useSSE hook
    return agents.find(a => a.id === agentId);
  };

  const isAgentActive = (agentId: string): boolean => {
    return activeAgents.includes(agentId);
  };

  // Filter messages
  const filteredMessages = messages.filter(message => {
    const matchesSearch = searchQuery === '' || 
      message.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
      getAgent(message.agent)?.name.toLowerCase().includes(searchQuery.toLowerCase());
    
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
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header with filters */}
      <Box
        sx={{
          p: 2,
          borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
          background: 'rgba(255, 255, 255, 0.02)',
        }}
      >
        <Stack spacing={2}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="h6" sx={{ fontWeight: 700, flex: 1 }}>
              Live Activity Feed
            </Typography>
            <Chip
              label={`${filteredMessages.length} messages`}
              size="small"
              sx={{
                background: 'rgba(139, 92, 246, 0.2)',
                color: '#a78bfa',
                fontWeight: 600,
              }}
            />
          </Box>

          {/* Search */}
          <TextField
            size="small"
            placeholder="Search messages..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
                </InputAdornment>
              ),
              endAdornment: searchQuery && (
                <InputAdornment position="end">
                  <IconButton size="small" onClick={() => setSearchQuery('')}>
                    <ClearIcon sx={{ fontSize: 18 }} />
                  </IconButton>
                </InputAdornment>
              ),
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                background: 'rgba(0, 0, 0, 0.2)',
              },
            }}
          />

          {/* Agent filters */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
            <Tooltip title="Filter by agent">
              <FilterListIcon sx={{ fontSize: 20, color: 'text.secondary' }} />
            </Tooltip>
            <Chip
              label="All"
              size="small"
              onClick={() => setSelectedAgent(null)}
              sx={{
                background: selectedAgent === null ? '#8b5cf6' : 'rgba(255, 255, 255, 0.05)',
                color: selectedAgent === null ? 'white' : 'text.secondary',
                fontWeight: 600,
                cursor: 'pointer',
                '&:hover': {
                  background: selectedAgent === null ? '#7c3aed' : 'rgba(255, 255, 255, 0.08)',
                },
              }}
            />
            {agents.map(agent => (
              <Chip
                key={agent.id}
                label={agent.name.split(' ')[0]}
                size="small"
                onClick={() => setSelectedAgent(agent.id === selectedAgent ? null : agent.id)}
                sx={{
                  background: selectedAgent === agent.id ? agent.color : 'rgba(255, 255, 255, 0.05)',
                  color: selectedAgent === agent.id ? 'white' : 'text.secondary',
                  fontWeight: 600,
                  cursor: 'pointer',
                  border: `1px solid ${agent.color}40`,
                  '&:hover': {
                    background: agent.color,
                    color: 'white',
                  },
                }}
              />
            ))}
          </Box>
        </Stack>
      </Box>

      {/* Message feed */}
      <Box
        ref={feedRef}
        onScroll={handleScroll}
        sx={{
          flex: 1,
          overflowY: 'auto',
          p: 2,
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
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
                      <Typography
                        variant="body2"
                        sx={{
                          color: 'text.primary',
                          lineHeight: 1.6,
                          whiteSpace: 'pre-wrap',
                        }}
                      >
                        {message.message}
                      </Typography>
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
  );
};

export default LiveActivityFeed;

