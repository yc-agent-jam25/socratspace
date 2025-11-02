/**
 * Bull vs Bear Arena Component
 * Gamified debate visualization: Bull vs Bear are the positions,
 * all agents contribute arguments supporting one side or the other
 */

import React, { useEffect, useState, useMemo } from 'react';
import { Box, Typography, Avatar, Tooltip, Chip, Stack } from '@mui/material';
import { keyframes } from '@mui/system';
import type { Agent, AgentMessage } from '../../lib/types';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

interface BullBearArenaProps {
  agents: Agent[];
  messages: AgentMessage[];
  activeAgents: string[];
}

const pulse = keyframes`
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
`;

const float = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
`;

const roar = keyframes`
  0%, 100% {
    transform: scale(1) rotate(0deg);
  }
  25% {
    transform: scale(1.2) rotate(-5deg);
  }
  75% {
    transform: scale(1.2) rotate(5deg);
  }
`;

// Analyze message content to determine sentiment
const analyzeMessageSentiment = (message: AgentMessage): 'bull' | 'bear' | 'neutral' => {
  const text = message.message.toLowerCase();
  
  // Bull indicators (optimistic, positive, growth, opportunity)
  const bullKeywords = [
    'strong', 'growth', 'opportunity', 'upside', 'excellent', 'positive', 'healthy',
    'proven', 'advantage', 'exceptional', 'bull', 'buy', 'invest', 'potential',
    'success', 'win', 'good', 'great', 'promising', 'solid', 'robust'
  ];
  
  // Bear indicators (risk, caution, concern, downside, problem)
  const bearKeywords = [
    'risk', 'caution', 'concern', 'problem', 'challenge', 'uncertainty', 'bear',
    'pass', 'downside', 'red flag', 'weak', 'limited', 'difficult', 'worried',
    'danger', 'threat', 'vulnerable', 'concern', 'issue', 'warning'
  ];
  
  // Check for explicit bull/bear mentions
  if (text.includes('🐂') || text.includes('bull') || text.includes('strong buy')) {
    return 'bull';
  }
  if (text.includes('🐻') || text.includes('bear') || text.includes('caution')) {
    return 'bear';
  }
  
  // Count keywords
  const bullCount = bullKeywords.filter(kw => text.includes(kw)).length;
  const bearCount = bearKeywords.filter(kw => text.includes(kw)).length;
  
  if (bullCount > bearCount && bullCount > 0) return 'bull';
  if (bearCount > bullCount && bearCount > 0) return 'bear';
  
  // Role-based hints
  if (message.agent === 'market_researcher' || message.agent === 'founder_evaluator' || message.agent === 'financial_analyst') {
    // These agents typically provide positive analysis
    return bullCount >= bearCount ? 'bull' : 'bear';
  }
  if (message.agent === 'risk_assessor' || message.agent === 'product_critic' || message.agent === 'brand_reputation') {
    // These agents typically identify concerns
    return bearCount >= bullCount ? 'bear' : 'bull';
  }
  
  return 'neutral';
};

const BullBearArena: React.FC<BullBearArenaProps> = ({
  agents,
  messages,
  activeAgents,
}) => {
  // Analyze all messages and categorize arguments
  const { bullArguments, bearArguments, neutralArguments } = useMemo(() => {
    const bull: AgentMessage[] = [];
    const bear: AgentMessage[] = [];
    const neutral: AgentMessage[] = [];
    
    messages.forEach(msg => {
      const sentiment = analyzeMessageSentiment(msg);
      if (sentiment === 'bull') bull.push(msg);
      else if (sentiment === 'bear') bear.push(msg);
      else neutral.push(msg);
    });
    
    return {
      bullArguments: bull,
      bearArguments: bear,
      neutralArguments: neutral,
    };
  }, [messages]);

  const bullScore = bullArguments.length;
  const bearScore = bearArguments.length;
  const totalScore = bullScore + bearScore || 1;
  const bullPercentage = (bullScore / totalScore) * 100;
  const bearPercentage = (bearScore / totalScore) * 100;

  // Get unique agents who contributed to each side
  const bullContributors = useMemo(() => {
    const agentIds = new Set(bullArguments.map(m => m.agent));
    return agents.filter(a => agentIds.has(a.id));
  }, [bullArguments, agents]);

  const bearContributors = useMemo(() => {
    const agentIds = new Set(bearArguments.map(m => m.agent));
    return agents.filter(a => agentIds.has(a.id));
  }, [bearArguments, agents]);

  const neutralContributors = useMemo(() => {
    const agentIds = new Set(neutralArguments.map(m => m.agent));
    return agents.filter(a => agentIds.has(a.id));
  }, [neutralArguments, agents]);

  // Get message counts per agent per side
  const getAgentBullCount = (agentId: string) => {
    return bullArguments.filter(m => m.agent === agentId).length;
  };

  const getAgentBearCount = (agentId: string) => {
    return bearArguments.filter(m => m.agent === agentId).length;
  };

  const getAgentTotalMessages = (agentId: string) => {
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
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background gradient overlay */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `linear-gradient(90deg, 
            rgba(16, 185, 129, 0.1) 0%, 
            rgba(16, 185, 129, 0.05) ${bullPercentage}%, 
            transparent ${bullPercentage}%, 
            transparent ${100 - bearPercentage}%,
            rgba(239, 68, 68, 0.05) ${100 - bearPercentage}%,
            rgba(239, 68, 68, 0.1) 100%
          )`,
          transition: 'all 1s ease',
          pointerEvents: 'none',
        }}
      />

      {/* Header with score */}
      <Box sx={{ position: 'relative', zIndex: 1, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
          <Typography
            variant="h5"
            sx={{
              fontWeight: 900,
              background: 'linear-gradient(90deg, #10b981 0%, #ef4444 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              textAlign: 'center',
              letterSpacing: '-0.02em',
            }}
          >
            ⚡ DEBATE ARENA ⚡
          </Typography>
        </Box>

        {/* Score display - Arguments count */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 2,
          }}
        >
          {/* Bull side */}
          <Box sx={{ flex: 1, textAlign: 'center' }}>
            <Box
              sx={{
                fontSize: '4rem',
                animation: bullScore > bearScore ? `${roar} 2s infinite` : 'none',
                filter: bullScore > bearScore ? 'drop-shadow(0 0 20px rgba(16, 185, 129, 0.5))' : 'none',
                transition: 'all 0.5s ease',
              }}
            >
              🐂
            </Box>
            <Typography
              variant="h3"
              sx={{
                fontWeight: 900,
                color: '#10b981',
                textShadow: bullScore > bearScore ? '0 0 20px rgba(16, 185, 129, 0.5)' : 'none',
              }}
            >
              {bullScore}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 600 }}>
              BULL ARGUMENTS
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.disabled', fontSize: '0.7rem' }}>
              {bullContributors.length} agent{bullContributors.length !== 1 ? 's' : ''} contributing
            </Typography>
          </Box>

          {/* VS divider */}
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 1,
            }}
          >
            <Typography
              variant="h4"
              sx={{
                fontWeight: 900,
                color: 'text.primary',
                px: 2,
                py: 1,
                background: 'rgba(255, 255, 255, 0.1)',
                borderRadius: 2,
                border: '2px solid rgba(255, 255, 255, 0.2)',
                animation: `${pulse} 2s infinite`,
              }}
            >
              VS
            </Typography>
            <Chip
              label={`${messages.length} total arguments`}
              size="small"
              sx={{
                background: 'rgba(139, 92, 246, 0.2)',
                color: '#a78bfa',
                fontWeight: 600,
                fontSize: '0.7rem',
              }}
            />
          </Box>

          {/* Bear side */}
          <Box sx={{ flex: 1, textAlign: 'center' }}>
            <Box
              sx={{
                fontSize: '4rem',
                animation: bearScore > bullScore ? `${roar} 2s infinite` : 'none',
                filter: bearScore > bullScore ? 'drop-shadow(0 0 20px rgba(239, 68, 68, 0.5))' : 'none',
                transition: 'all 0.5s ease',
              }}
            >
              🐻
            </Box>
            <Typography
              variant="h3"
              sx={{
                fontWeight: 900,
                color: '#ef4444',
                textShadow: bearScore > bullScore ? '0 0 20px rgba(239, 68, 68, 0.5)' : 'none',
              }}
            >
              {bearScore}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 600 }}>
              BEAR ARGUMENTS
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.disabled', fontSize: '0.7rem' }}>
              {bearContributors.length} agent{bearContributors.length !== 1 ? 's' : ''} contributing
            </Typography>
          </Box>
        </Box>
      </Box>

      {/* Sentiment meter */}
      <Box sx={{ position: 'relative', zIndex: 1, mb: 3 }}>
        <Box
          sx={{
            height: 8,
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: 4,
            overflow: 'hidden',
            position: 'relative',
          }}
        >
          <Box
            sx={{
              position: 'absolute',
              left: 0,
              top: 0,
              height: '100%',
              width: `${bullPercentage}%`,
              background: 'linear-gradient(90deg, #10b981 0%, #34d399 100%)',
              transition: 'width 1s ease',
              boxShadow: '0 0 20px rgba(16, 185, 129, 0.5)',
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              right: 0,
              top: 0,
              height: '100%',
              width: `${bearPercentage}%`,
              background: 'linear-gradient(90deg, #f87171 0%, #ef4444 100%)',
              transition: 'width 1s ease',
              boxShadow: '0 0 20px rgba(239, 68, 68, 0.5)',
            }}
          />
        </Box>
      </Box>

      {/* All Agents contributing to the debate */}
      <Box sx={{ position: 'relative', zIndex: 1 }}>
        <Typography
          variant="body2"
          sx={{
            textAlign: 'center',
            color: 'text.secondary',
            fontWeight: 600,
            mb: 2,
            textTransform: 'uppercase',
            fontSize: '0.75rem',
            letterSpacing: '0.05em',
          }}
        >
          🏛️ Council Members Contributing to the Debate
        </Typography>

        {/* All agents in a grid, showing their contributions to each side */}
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: { xs: 'repeat(2, 1fr)', sm: 'repeat(4, 1fr)', md: 'repeat(4, 1fr)' },
            gap: 2,
          }}
        >
          {agents.map((agent) => {
            const isActive = activeAgents.includes(agent.id);
            const bullCount = getAgentBullCount(agent.id);
            const bearCount = getAgentBearCount(agent.id);
            const totalCount = getAgentTotalMessages(agent.id);
            const hasContributions = bullCount > 0 || bearCount > 0;

            return (
              <Tooltip
                key={agent.id}
                title={
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 700 }}>
                      {agent.name}
                    </Typography>
                    {bullCount > 0 && (
                      <Typography variant="caption" sx={{ display: 'block', color: '#10b981' }}>
                        🐂 {bullCount} bull argument{bullCount !== 1 ? 's' : ''}
                      </Typography>
                    )}
                    {bearCount > 0 && (
                      <Typography variant="caption" sx={{ display: 'block', color: '#ef4444' }}>
                        🐻 {bearCount} bear argument{bearCount !== 1 ? 's' : ''}
                      </Typography>
                    )}
                    {totalCount === 0 && (
                      <Typography variant="caption" sx={{ display: 'block', color: 'text.secondary' }}>
                        ⏳ Waiting to contribute
                      </Typography>
                    )}
                  </Box>
                }
                arrow
              >
                <Box
                  sx={{
                    position: 'relative',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    p: 1.5,
                    borderRadius: 2,
                    background: hasContributions
                      ? 'rgba(255, 255, 255, 0.03)'
                      : 'rgba(255, 255, 255, 0.01)',
                    border: `1px solid ${hasContributions ? 'rgba(255, 255, 255, 0.1)' : 'rgba(255, 255, 255, 0.05)'}`,
                    transition: 'all 0.3s ease',
                    animation: isActive ? `${float} 2s infinite` : 'none',
                    '&:hover': {
                      background: 'rgba(255, 255, 255, 0.05)',
                      transform: 'translateY(-2px)',
                    },
                  }}
                >
                  <Avatar
                    sx={{
                      width: 56,
                      height: 56,
                      bgcolor: agent.color,
                      border: bullCount > bearCount
                        ? '2px solid #10b981'
                        : bearCount > bullCount
                        ? '2px solid #ef4444'
                        : bullCount === bearCount && bullCount > 0
                        ? '2px solid #f59e0b'
                        : '2px solid rgba(255, 255, 255, 0.2)',
                      boxShadow: isActive
                        ? bullCount > bearCount
                          ? '0 0 20px rgba(16, 185, 129, 0.6)'
                          : bearCount > bullCount
                          ? '0 0 20px rgba(239, 68, 68, 0.6)'
                          : '0 0 20px rgba(139, 92, 246, 0.6)'
                        : 'none',
                      mb: 1,
                    }}
                  >
                    {agent.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
                  </Avatar>

                  {/* Agent name */}
                  <Typography
                    variant="caption"
                    sx={{
                      color: 'text.secondary',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textAlign: 'center',
                      mb: 0.5,
                      maxWidth: '100%',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {agent.name.split(' ')[0]}
                  </Typography>

                  {/* Contribution badges */}
                  <Stack direction="row" spacing={0.5} sx={{ alignItems: 'center' }}>
                    {bullCount > 0 && (
                      <Chip
                        label={bullCount}
                        size="small"
                        sx={{
                          height: 18,
                          fontSize: '0.6rem',
                          fontWeight: 700,
                          background: '#10b981',
                          color: 'white',
                          minWidth: 20,
                        }}
                      />
                    )}
                    {bearCount > 0 && (
                      <Chip
                        label={bearCount}
                        size="small"
                        sx={{
                          height: 18,
                          fontSize: '0.6rem',
                          fontWeight: 700,
                          background: '#ef4444',
                          color: 'white',
                          minWidth: 20,
                        }}
                      />
                    )}
                    {totalCount === 0 && (
                      <Box
                        sx={{
                          width: 6,
                          height: 6,
                          borderRadius: '50%',
                          background: '#6b7280',
                        }}
                      />
                    )}
                  </Stack>
                </Box>
              </Tooltip>
            );
          })}
        </Box>
      </Box>

      {/* Victory indicator */}
      {bullScore !== bearScore && messages.length > 5 && (
        <Box
          sx={{
            position: 'relative',
            zIndex: 1,
            mt: 3,
            textAlign: 'center',
          }}
        >
          <Chip
            label={
              bullScore > bearScore
                ? `🐂 Bull Case Leading by ${bullScore - bearScore} argument${bullScore - bearScore !== 1 ? 's' : ''}`
                : `🐻 Bear Case Leading by ${bearScore - bullScore} argument${bearScore - bullScore !== 1 ? 's' : ''}`
            }
            sx={{
              background: bullScore > bearScore
                ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.3) 100%)'
                : 'linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.3) 100%)',
              color: bullScore > bearScore ? '#10b981' : '#ef4444',
              fontWeight: 700,
              fontSize: '0.875rem',
              px: 2,
              py: 1,
              height: 'auto',
              border: bullScore > bearScore
                ? '1px solid rgba(16, 185, 129, 0.3)'
                : '1px solid rgba(239, 68, 68, 0.3)',
              animation: `${pulse} 2s infinite`,
            }}
          />
        </Box>
      )}
    </Box>
  );
};

export default BullBearArena;
