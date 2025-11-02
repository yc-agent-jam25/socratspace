/**
 * CTA Section Component
 * Bottom call-to-action section
 */

import React from 'react';
import { Box, Container, Typography, Button, Stack } from '@mui/material';
import { keyframes } from '@mui/system';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';

interface CTASectionProps {
  onGetStarted: () => void;
}

const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
`;

const CTASection: React.FC<CTASectionProps> = ({ onGetStarted }) => {
  return (
    <Box
      sx={{
        py: { xs: 10, md: 15 },
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background glow */}
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '80%',
          height: '80%',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%)',
          filter: 'blur(80px)',
          zIndex: 0,
        }}
      />

      <Container maxWidth="md" sx={{ position: 'relative', zIndex: 1 }}>
        <Box
          sx={{
            textAlign: 'center',
            p: { xs: 4, md: 8 },
            borderRadius: 4,
            background: 'rgba(255, 255, 255, 0.05)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
          }}
        >
          {/* Floating rocket icon */}
          <Box
            sx={{
              fontSize: '4rem',
              mb: 3,
              animation: `${float} 3s ease-in-out infinite`,
            }}
          >
            🚀
          </Box>

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
            Ready to Transform Your Deal Flow?
          </Typography>

          <Typography
            variant="h6"
            sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              mb: 4,
              fontWeight: 400,
              lineHeight: 1.6,
            }}
          >
            Join forward-thinking VCs using AI to make faster, better investment decisions
          </Typography>

          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={2}
            justifyContent="center"
          >
            <Button
              variant="contained"
              size="large"
              startIcon={<RocketLaunchIcon />}
              onClick={onGetStarted}
              sx={{
                py: 2,
                px: 5,
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
              Analyze Your First Deal
            </Button>
          </Stack>

          {/* Trust indicators */}
          <Stack
            direction="row"
            spacing={4}
            justifyContent="center"
            sx={{ mt: 5, flexWrap: 'wrap', gap: 2 }}
          >
            {[
              '✓ No credit card required',
              '✓ 5-minute setup',
              '✓ Free analysis',
            ].map((text, index) => (
              <Typography
                key={index}
                variant="body2"
                sx={{
                  color: 'rgba(255, 255, 255, 0.5)',
                  fontWeight: 500,
                  fontSize: '0.875rem',
                }}
              >
                {text}
              </Typography>
            ))}
          </Stack>
        </Box>
      </Container>

      {/* Footer */}
      <Box sx={{ textAlign: 'center', mt: 10 }}>
        <Typography
          variant="body2"
          sx={{
            color: 'rgba(255, 255, 255, 0.4)',
            fontSize: '0.875rem',
          }}
        >
          © 2025 Socrat Space. Powered by AI, driven by insight.
        </Typography>
      </Box>
    </Box>
  );
};

export default CTASection;

