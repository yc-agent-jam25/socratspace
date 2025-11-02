/**
 * Custom hook for managing debate simulation
 */

import { useState, useCallback, useEffect } from 'react';
import type { Phase, AgentMessage, Decision } from '../lib/types';
import { simulationService } from '../lib/simulation';

interface UseSimulationReturn {
  phase: Phase;
  messages: AgentMessage[];
  decision: Decision | null;
  isRunning: boolean;
  elapsedTime: number;
  startSimulation: () => void;
  resetSimulation: () => void;
}

export const useSimulation = (): UseSimulationReturn => {
  const [phase, setPhase] = useState<Phase>('idle');
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const [decision, setDecision] = useState<Decision | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);

  // Update elapsed time every second
  useEffect(() => {
    if (!isRunning || !startTime) return;

    const interval = setInterval(() => {
      setElapsedTime(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning, startTime]);

  const startSimulation = useCallback(() => {
    // Reset state
    setPhase('idle');
    setMessages([]);
    setDecision(null);
    setIsRunning(true);
    setElapsedTime(0);
    setStartTime(Date.now());

    // Start simulation
    simulationService.start({
      onPhaseChange: (newPhase) => {
        setPhase(newPhase);
      },
      onMessage: (message) => {
        setMessages((prev) => [...prev, message]);
      },
      onDecision: (dec) => {
        setDecision(dec);
      },
      onComplete: () => {
        setIsRunning(false);
      }
    });
  }, []);

  const resetSimulation = useCallback(() => {
    simulationService.reset();
    setPhase('idle');
    setMessages([]);
    setDecision(null);
    setIsRunning(false);
    setElapsedTime(0);
    setStartTime(null);
  }, []);

  return {
    phase,
    messages,
    decision,
    isRunning,
    elapsedTime,
    startSimulation,
    resetSimulation
  };
};

