/**
 * Hero Section Component
 * Modern landing page hero with compelling CTA
 */

import React from 'react';
import { Box, Typography, Button, Container, Stack } from '@mui/material';
import { keyframes } from '@mui/system';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import Logo from './Logo';

interface HeroSectionProps {
  onGetStarted: () => void;
}

const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
`;

const HeroSection: React.FC<HeroSectionProps> = ({ onGetStarted }) => {
  return (
    <Box
      sx={{
        position: 'relative',
        py: { xs: 4, md: 5 },
        overflow: 'hidden',
      }}
    >
      {/* Animated background orbs */}
      <Box
        sx={{
          position: 'absolute',
          top: '20%',
          right: '10%',
          width: 400,
          height: 400,
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%)',
          filter: 'blur(60px)',
          animation: `${float} 6s ease-in-out infinite`,
          zIndex: 0,
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          bottom: '20%',
          left: '5%',
          width: 350,
          height: 350,
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%)',
          filter: 'blur(60px)',
          animation: `${float} 8s ease-in-out infinite`,
          animationDelay: '1s',
          zIndex: 0,
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          width: 300,
          height: 300,
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%)',
          filter: 'blur(60px)',
          animation: `${float} 7s ease-in-out infinite`,
          animationDelay: '2s',
          zIndex: 0,
        }}
      />

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        <Box sx={{ textAlign: 'center', maxWidth: 900, mx: 'auto' }}>
          {/* Logo */}
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              mb: 0,
              animation: 'fadeInUp 0.6s ease-out',
            }}
          >
            <Logo 
              size={280}
              sx={{
                '@media (max-width: 600px)': {
                  width: 200,
                  height: 200,
                },
              }}
            />
          </Box>

          {/* Main headline */}
          <Typography
            variant="h1"
            sx={{
              fontSize: { xs: '3rem', sm: '4rem', md: '5rem' },
              fontWeight: 900,
              lineHeight: 1,
              mt: -3,
              mb: 3,
              background: 'linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #ffffff 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.04em',
              animation: 'fadeInUp 0.8s ease-out',
              animationDelay: '0.1s',
              animationFillMode: 'backwards',
            }}
          >
            Socrat Space
          </Typography>
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: '1.5rem', sm: '2rem', md: '2.5rem' },
              fontWeight: 600,
              lineHeight: 1.2,
              mb: 2,
              color: 'rgba(255, 255, 255, 0.9)',
              letterSpacing: '-0.02em',
              animation: 'fadeInUp 0.8s ease-out',
              animationDelay: '0.2s',
              animationFillMode: 'backwards',
            }}
          >
            AI Agents Debate Your Investment Decisions
          </Typography>

          {/* Subheadline */}
          <Typography
            variant="h5"
            sx={{
              fontSize: { xs: '1.125rem', md: '1.5rem' },
              fontWeight: 400,
              color: 'rgba(255, 255, 255, 0.75)',
              mb: 3,
              lineHeight: 1.6,
              maxWidth: 700,
              mx: 'auto',
              animation: 'fadeInUp 1s ease-out',
              animationDelay: '0.2s',
              animationFillMode: 'backwards',
            }}
          >
            From pitch deck to calendar invite in minutes. Watch specialized AI agents analyze markets, 
            evaluate founders, assess finances, and debate investment decisions in real-time.
          </Typography>

          {/* CTA Buttons */}
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={2}
            justifyContent="center"
            sx={{
              mb: 3,
              animation: 'fadeInUp 1.2s ease-out',
              animationDelay: '0.3s',
              animationFillMode: 'backwards',
            }}
          >
            <Button
              variant="contained"
              size="large"
              endIcon={<ArrowForwardIcon />}
              onClick={onGetStarted}
              sx={{
                py: 2,
                px: 4,
                fontSize: '1.125rem',
                fontWeight: 700,
                borderRadius: 2,
                background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                boxShadow: '0 8px 32px rgba(59, 130, 246, 0.4)',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  boxShadow: '0 12px 48px rgba(59, 130, 246, 0.6)',
                  background: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
                },
              }}
            >
              Start Free Analysis
            </Button>
            <Button
              variant="outlined"
              size="large"
              startIcon={<PlayArrowIcon />}
              sx={{
                py: 2,
                px: 4,
                fontSize: '1.125rem',
                fontWeight: 600,
                borderRadius: 2,
                borderColor: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                backdropFilter: 'blur(10px)',
                background: 'rgba(255, 255, 255, 0.05)',
                transition: 'all 0.3s ease',
                '&:hover': {
                  borderColor: 'rgba(255, 255, 255, 0.4)',
                  background: 'rgba(255, 255, 255, 0.1)',
                  transform: 'translateY(-2px)',
                },
              }}
            >
              Watch Demo
            </Button>
          </Stack>

          {/* Stats */}
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={{ xs: 2, sm: 4 }}
            justifyContent="center"
            sx={{
              mb: 0,
              animation: 'fadeInUp 1.4s ease-out',
              animationDelay: '0.4s',
              animationFillMode: 'backwards',
            }}
          >
            {[
              { value: '<15min', label: 'Analysis Time' },
              { value: '100%', label: 'Transparent' },
              { value: '4', label: 'Deliberation Rounds' },
            ].map((stat, index) => (
              <Box
                key={index}
                sx={{
                  textAlign: 'center',
                  px: 3,
                  py: 2,
                  borderRadius: 2,
                  background: 'rgba(255, 255, 255, 0.03)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.05)',
                }}
              >
                <Typography
                  variant="h3"
                  sx={{
                    fontWeight: 800,
                    background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    mb: 0.5,
                  }}
                >
                  {stat.value}
                </Typography>
                <Typography
                  variant="body2"
                  sx={{
                    color: 'rgba(255, 255, 255, 0.6)',
                    fontWeight: 500,
                    textTransform: 'uppercase',
                    letterSpacing: '0.1em',
                    fontSize: '0.75rem',
                  }}
                >
                  {stat.label}
                </Typography>
              </Box>
            ))}
          </Stack>

        </Box>
      </Container>
    </Box>
  );
};

export default HeroSection;

