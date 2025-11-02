/**
 * Phase Indicator Component
 * Shows current phase of debate (Research, Debate, Decision)
 */

import React from 'react';
import { Box, Stepper, Step, StepLabel } from '@mui/material';
import type { Phase } from '../lib/types';

interface PhaseIndicatorProps {
  currentPhase: Phase;
}

const phases = [
  { id: 'research', label: 'Research' },
  { id: 'debate', label: 'Debate' },
  { id: 'decision', label: 'Decision' }
];

const PhaseIndicator: React.FC<PhaseIndicatorProps> = ({ currentPhase }) => {
  // Map phase to step index
  const getActiveStep = (): number => {
    if (currentPhase === 'idle') return -1;
    if (currentPhase === 'research') return 0;
    if (currentPhase === 'debate') return 1;
    if (currentPhase === 'decision') return 2;
    if (currentPhase === 'completed') return 3;
    return -1;
  };

  const activeStep = getActiveStep();

  return (
    <Box sx={{ 
      mb: 4,
      animation: 'fadeIn 0.5s ease-in'
    }}>
      <Stepper 
        activeStep={activeStep}
        sx={{
          '& .MuiStepLabel-root .Mui-completed': {
            color: 'success.main'
          },
          '& .MuiStepLabel-root .Mui-active': {
            color: 'primary.main',
            fontWeight: 600
          },
          '& .MuiStepIcon-root.Mui-active': {
            animation: 'pulse 1.5s infinite',
            '@keyframes pulse': {
              '0%, 100%': {
                transform: 'scale(1)'
              },
              '50%': {
                transform: 'scale(1.1)'
              }
            }
          }
        }}
      >
        {phases.map((phase, index) => (
          <Step key={phase.id} completed={activeStep > index}>
            <StepLabel>{phase.label}</StepLabel>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
};

export default PhaseIndicator;
