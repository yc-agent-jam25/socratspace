/**
 * Landing Page Component
 * Complete landing experience with hero, features, and how it works
 */

import React from 'react';
import { Box } from '@mui/material';
import HeroSection from './HeroSection';
import FeaturesSection from './FeaturesSection';
import HowItWorksSection from './HowItWorksSection';
import CTASection from './CTASection';

interface LandingPageProps {
  onGetStarted: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
  return (
    <Box>
      <HeroSection onGetStarted={onGetStarted} />
      <FeaturesSection />
      <HowItWorksSection />
      <CTASection onGetStarted={onGetStarted} />
    </Box>
  );
};

export default LandingPage;

