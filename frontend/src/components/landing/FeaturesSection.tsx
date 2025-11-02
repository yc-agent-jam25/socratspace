/**
 * Features Section Component
 * Showcase key features and benefits
 */

import React from 'react';
import { Box, Container, Typography, Grid, Stack } from '@mui/material';

// Icons
import PsychologyIcon from '@mui/icons-material/Psychology';
import SpeedIcon from '@mui/icons-material/Speed';
import BalanceIcon from '@mui/icons-material/Balance';
import InsightsIcon from '@mui/icons-material/Insights';
import GroupsIcon from '@mui/icons-material/Groups';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

interface Feature {
  icon: React.ReactElement;
  title: string;
  description: string;
  color: string;
}

const features: Feature[] = [
  {
    icon: <PsychologyIcon sx={{ fontSize: 40 }} />,
    title: 'Multi-Agent Deliberation',
    description: 'Specialized AI agents analyze every angle: market fit, founder quality, financial viability, and risk assessment.',
    color: '#3b82f6',
  },
  {
    icon: <SpeedIcon sx={{ fontSize: 40 }} />,
    title: 'Fast Analysis',
    description: 'Get comprehensive investment insights in less than 20 minutes. From input to decision faster than traditional partner meetings.',
    color: '#10b981',
  },
  {
    icon: <BalanceIcon sx={{ fontSize: 40 }} />,
    title: 'Bull vs Bear Debate',
    description: 'Watch optimistic and skeptical agents argue opposing viewpoints before the Lead Partner makes the final call.',
    color: '#f59e0b',
  },
  {
    icon: <InsightsIcon sx={{ fontSize: 40 }} />,
    title: 'Transparent Reasoning',
    description: 'See every step of the decision-making process. Full visibility into each agent\'s analysis and conclusions.',
    color: '#8b5cf6',
  },
  {
    icon: <GroupsIcon sx={{ fontSize: 40 }} />,
    title: 'Council Chamber View',
    description: 'Beautiful visualization of the debate flow. Watch agents transition from research to debate to final decision.',
    color: '#ec4899',
  },
  {
    icon: <AutoAwesomeIcon sx={{ fontSize: 40 }} />,
    title: 'Actionable Outputs',
    description: 'Get investment memos, calendar invites, and structured decisions ready to share with your team.',
    color: '#06b6d4',
  },
];

const FeaturesSection: React.FC = () => {
  return (
    <Box
      sx={{
        py: { xs: 6, md: 8 },
        position: 'relative',
      }}
    >
      <Container maxWidth="lg">
        {/* Section Header */}
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography
            variant="overline"
            sx={{
              color: '#3b82f6',
              fontWeight: 700,
              letterSpacing: '0.15em',
              fontSize: '0.875rem',
              mb: 2,
              display: 'block',
            }}
          >
            FEATURES
          </Typography>
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: '2rem', md: '3rem' },
              fontWeight: 800,
              mb: 2,
              background: 'linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.02em',
            }}
          >
            AI-Powered Investment Intelligence
          </Typography>
          <Typography
            variant="h6"
            sx={{
              color: 'rgba(255, 255, 255, 0.6)',
              maxWidth: 600,
              mx: 'auto',
              fontWeight: 400,
            }}
          >
            Everything you need to make faster, more informed investment decisions
          </Typography>
        </Box>

        {/* Features Grid */}
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={6} lg={4} key={index}>
              <Box
                sx={{
                  height: '100%',
                  p: 4,
                  borderRadius: 3,
                  background: 'rgba(255, 255, 255, 0.03)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                  cursor: 'default',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    background: 'rgba(255, 255, 255, 0.05)',
                    borderColor: `${feature.color}40`,
                    boxShadow: `0 20px 60px ${feature.color}30`,
                    '& .feature-icon': {
                      transform: 'scale(1.1) rotate(5deg)',
                      background: `linear-gradient(135deg, ${feature.color} 0%, ${feature.color}CC 100%)`,
                    },
                  },
                }}
              >
                <Stack spacing={2}>
                  {/* Icon */}
                  <Box
                    className="feature-icon"
                    sx={{
                      width: 64,
                      height: 64,
                      borderRadius: 2,
                      background: `${feature.color}20`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: feature.color,
                      transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                      border: `1px solid ${feature.color}40`,
                    }}
                  >
                    {feature.icon}
                  </Box>

                  {/* Content */}
                  <Box>
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: 700,
                        mb: 1,
                        color: 'text.primary',
                      }}
                    >
                      {feature.title}
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{
                        color: 'rgba(255, 255, 255, 0.65)',
                        lineHeight: 1.7,
                      }}
                    >
                      {feature.description}
                    </Typography>
                  </Box>
                </Stack>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default FeaturesSection;

