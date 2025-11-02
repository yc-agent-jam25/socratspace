/**
 * CouncilChamber Component
 * Main component that switches between different layouts based on phase
 */

import React, { useState, useEffect } from 'react';
import { Box } from '@mui/material';
import type { Phase, Agent, AgentMessage } from '../../lib/types';
import RoundTableLayout from './RoundTableLayout';
import CourtroomLayout from './CourtroomLayout';
import SummitLayout from './SummitLayout';

interface CouncilChamberProps {
  phase: Phase;
  agents: Agent[];
  messages: AgentMessage[];
  activeAgents: string[];
  onAgentClick?: (agent: Agent) => void;
}

const CouncilChamber: React.FC<CouncilChamberProps> = ({
  phase,
  agents,
  messages,
  activeAgents,
  onAgentClick,
}) => {
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Update container size on mount and resize
  useEffect(() => {
    const updateSize = () => {
      // Get the viewport dimensions
      const width = window.innerWidth;
      const height = window.innerHeight;
      setContainerSize({ width: width - 100, height: Math.max(height - 300, 600) });
    };

    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  // Handle phase transitions
  useEffect(() => {
    setIsTransitioning(true);
    const timer = setTimeout(() => setIsTransitioning(false), 600);
    return () => clearTimeout(timer);
  }, [phase]);

  // Separate agents by role
  const researchAgents = agents.filter(a =>
    ['market_researcher', 'founder_evaluator', 'product_critic', 'financial_analyst', 'risk_assessor'].includes(a.id)
  );
  const bullAgent = agents.find(a => a.id === 'bull_agent');
  const bearAgent = agents.find(a => a.id === 'bear_agent');
  const leadPartner = agents.find(a => a.id === 'lead_partner');

  // Render the appropriate layout based on phase
  const renderLayout = () => {
    if (!containerSize.width || !containerSize.height) {
      return null; // Wait for size calculation
    }

    switch (phase) {
      case 'research':
        return (
          <RoundTableLayout
            agents={researchAgents}
            messages={messages}
            activeAgents={activeAgents}
            onAgentClick={onAgentClick}
            containerWidth={containerSize.width}
            containerHeight={containerSize.height}
          />
        );

      case 'debate':
        if (!bullAgent || !bearAgent) return null;
        return (
          <CourtroomLayout
            bullAgent={bullAgent}
            bearAgent={bearAgent}
            observerAgents={researchAgents}
            messages={messages}
            activeAgents={activeAgents}
            onAgentClick={onAgentClick}
            containerWidth={containerSize.width}
            containerHeight={containerSize.height}
          />
        );

      case 'decision':
        if (!leadPartner) return null;
        return (
          <SummitLayout
            leadPartner={leadPartner}
            researchAgents={researchAgents}
            messages={messages}
            activeAgents={activeAgents}
            onAgentClick={onAgentClick}
            containerWidth={containerSize.width}
            containerHeight={containerSize.height}
          />
        );

      default:
        return null;
    }
  };

  return (
    <Box
      sx={{
        width: '100%',
        minHeight: 600,
        position: 'relative',
        overflow: 'hidden',
        borderRadius: 3,
        background: 'rgba(255, 255, 255, 0.02)',
        border: '1px solid rgba(255, 255, 255, 0.05)',
        backdropFilter: 'blur(10px)',
        transition: 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
        opacity: isTransitioning ? 0.5 : 1,
        transform: isTransitioning ? 'scale(0.98)' : 'scale(1)',
      }}
    >
      {renderLayout()}
    </Box>
  );
};

export default CouncilChamber;

