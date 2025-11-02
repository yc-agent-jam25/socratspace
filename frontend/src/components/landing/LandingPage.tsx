/**
 * Landing Page Component
 * Complete landing experience with hero, features, results, and architecture
 */

import React from 'react';
import { Box } from '@mui/material';
import HeroSection from './HeroSection';
import FeaturesSection from './FeaturesSection';
import ResultsSection from './ResultsSection';
import SystemArchitectureSection from './SystemArchitectureSection';
import CTASection from './CTASection';

interface LandingPageProps {
  onGetStarted: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
  return (
    <Box>
      <HeroSection onGetStarted={onGetStarted} />
      <FeaturesSection />
      <ResultsSection />
      <SystemArchitectureSection />
      <CTASection onGetStarted={onGetStarted} />
    </Box>
  );
};

export default LandingPage;

