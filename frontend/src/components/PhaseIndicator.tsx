/**
 * Phase Indicator Component
 * Shows current phase of debate (Research, Debate, Decision)
 * TODO: Implement phase visualization
 */

import React from 'react';

interface PhaseIndicatorProps {
  currentPhase: string;
}

const PhaseIndicator: React.FC<PhaseIndicatorProps> = ({ currentPhase }) => {
  // TODO: Implement stepper/progress indicator
  // Phases: research -> debate -> decision

  return (
    <div>
      <h3>TODO: Phase Indicator</h3>
      <p>Current Phase: {currentPhase}</p>
    </div>
  );
};

export default PhaseIndicator;
