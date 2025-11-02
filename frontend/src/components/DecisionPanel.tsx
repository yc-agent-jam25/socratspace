/**
 * Decision Panel Component
 * Displays final investment decision and memo
 * TODO: Implement decision display
 */

import React from 'react';
import type { Decision } from '../lib/types';

interface DecisionPanelProps {
  decision: Decision;
}

const DecisionPanel: React.FC<DecisionPanelProps> = ({ decision }) => {
  // TODO: Implement decision display
  // TODO: Show decision (PASS/MAYBE/INVEST) with color coding
  // TODO: Display reasoning
  // TODO: Render investment memo (markdown)
  // TODO: Show calendar events created

  return (
    <div>
      <h2>Final Decision: {decision.decision}</h2>
      <p>TODO: Display reasoning and investment memo</p>
      <p>TODO: Show {decision.calendar_events.length} calendar events created</p>
    </div>
  );
};

export default DecisionPanel;
