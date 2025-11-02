/**
 * How It Works Section
 * Step-by-step process visualization
 */

import React from 'react';
import { Box, Container, Typography, Stack } from '@mui/material';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

interface Step {
  number: string;
  title: string;
  description: string;
  icon: string;
  color: string;
}

const steps: Step[] = [
  {
    number: '01',
    title: 'Submit Company Info',
    description: 'Enter basic details about the startup: name, industry, stage, and pitch deck URL.',
    icon: '📝',
    color: '#3b82f6',
  },
  {
    number: '02',
    title: 'Research Phase',
    description: 'Specialized agents analyze market, founders, product, financials, and risks simultaneously.',
    icon: '🔍',
    color: '#10b981',
  },
  {
    number: '03',
    title: 'Bull vs Bear Debate',
    description: 'Optimistic and skeptical agents present opposing arguments. Watch the deliberation unfold.',
    icon: '⚖️',
    color: '#f59e0b',
  },
  {
    number: '04',
    title: 'Final Decision',
    description: 'Lead Partner reviews all evidence and delivers: Invest, Maybe, or Pass with detailed reasoning.',
    icon: '✅',
    color: '#8b5cf6',
  },
];

const HowItWorksSection: React.FC = () => {
  return (
    <Box
      sx={{
        py: { xs: 10, md: 15 },
        position: 'relative',
        background: 'rgba(255, 255, 255, 0.02)',
      }}
    >
      <Container maxWidth="lg">
        {/* Section Header */}
        <Box sx={{ textAlign: 'center', mb: 10 }}>
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
            HOW IT WORKS
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
            Four Phases to Better Decisions
          </Typography>
        </Box>

        {/* Steps */}
        <Stack spacing={6}>
          {steps.map((step, index) => (
            <Box key={index}>
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: { xs: 'column', md: 'row' },
                  gap: 4,
                  alignItems: { md: 'center' },
                  p: 4,
                  borderRadius: 3,
                  background: 'rgba(255, 255, 255, 0.03)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  transition: 'all 0.4s ease',
                  '&:hover': {
                    transform: 'translateX(8px)',
                    borderColor: `${step.color}40`,
                    boxShadow: `0 12px 48px ${step.color}20`,
                    background: 'rgba(255, 255, 255, 0.05)',
                  },
                }}
              >
                {/* Step Number & Icon */}
                <Box
                  sx={{
                    flexShrink: 0,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 3,
                  }}
                >
                  <Box
                    sx={{
                      width: 80,
                      height: 80,
                      borderRadius: 2,
                      background: `linear-gradient(135deg, ${step.color}20 0%, ${step.color}10 100%)`,
                      border: `2px solid ${step.color}40`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '2.5rem',
                      flexShrink: 0,
                    }}
                  >
                    {step.icon}
                  </Box>
                  <Typography
                    variant="h2"
                    sx={{
                      fontWeight: 900,
                      color: `${step.color}40`,
                      fontSize: '4rem',
                      lineHeight: 1,
                      display: { xs: 'none', sm: 'block' },
                    }}
                  >
                    {step.number}
                  </Typography>
                </Box>

                {/* Content */}
                <Box sx={{ flex: 1 }}>
                  <Typography
                    variant="h5"
                    sx={{
                      fontWeight: 700,
                      mb: 1,
                      color: 'text.primary',
                    }}
                  >
                    {step.title}
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.7)',
                      lineHeight: 1.8,
                    }}
                  >
                    {step.description}
                  </Typography>
                </Box>

                {/* Arrow (hidden on mobile) */}
                {index < steps.length - 1 && (
                  <ArrowForwardIcon
                    sx={{
                      display: { xs: 'none', lg: 'block' },
                      color: step.color,
                      fontSize: 32,
                      flexShrink: 0,
                    }}
                  />
                )}
              </Box>

              {/* Connecting line */}
              {index < steps.length - 1 && (
                <Box
                  sx={{
                    width: 2,
                    height: 40,
                    background: `linear-gradient(180deg, ${step.color}40 0%, ${steps[index + 1].color}40 100%)`,
                    mx: { xs: 2, md: 6 },
                    my: 2,
                  }}
                />
              )}
            </Box>
          ))}
        </Stack>
      </Container>
    </Box>
  );
};

export default HowItWorksSection;

