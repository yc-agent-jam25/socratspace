/**
 * Custom hook for managing debate simulation
 * Can use SSE for real-time updates or mock simulation for development
 */

import { useState, useCallback, useEffect } from 'react';
import type { Phase, AgentMessage, Decision } from '../lib/types';
import { simulationService } from '../lib/simulation';
import { useSSE as useSSEHook } from './useSSE';

interface OAuthRequest {
  mcp_name: string;
  auth_url: string;
  oauth_session_id: string;
  timestamp?: string;
}

interface UseSimulationReturn {
  phase: Phase;
  messages: AgentMessage[];
  decision: Decision | null;
  isRunning: boolean;
  elapsedTime: number;
  connectionStatus?: 'connecting' | 'connected' | 'disconnected' | 'error';
  error?: string | null;
  oauthRequest?: OAuthRequest | null;
  startSimulation: () => void;
  resetSimulation: () => void;
  reconnect?: () => void;
}

interface UseSimulationOptions {
  sessionId?: string | null;
  useSSE?: boolean; // If true, use SSE instead of mock simulation
}

export const useSimulation = (options: UseSimulationOptions = {}): UseSimulationReturn => {
  const { sessionId = null, useSSE = false } = options;
  // Use SSE if enabled and sessionId provided, otherwise use mock simulation
  const shouldUseSSE = useSSE && !!sessionId;
  const sse = useSSEHook(sessionId, shouldUseSSE);
  
  const [phase, setPhase] = useState<Phase>('idle');
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const [decision, setDecision] = useState<Decision | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  
  // Sync SSE state when using SSE
  useEffect(() => {
    if (shouldUseSSE) {
      setPhase(sse.phase);
      setMessages(sse.messages);
      setDecision(sse.decision);
      setIsRunning(sse.phase !== 'completed' && sse.phase !== 'idle');
    }
  }, [shouldUseSSE, sse.phase, sse.messages, sse.decision]);

  // Update elapsed time every second
  useEffect(() => {
    if (!isRunning || !startTime) return;

    const interval = setInterval(() => {
      setElapsedTime(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning, startTime]);

  const startSimulation = useCallback(() => {
    // If using SSE, don't start mock simulation
    if (shouldUseSSE) {
      // SSE will handle state updates automatically
      setIsRunning(true);
      setStartTime(Date.now());
      return;
    }

    // Reset state
    setPhase('idle');
    setMessages([]);
    setDecision(null);
    setIsRunning(true);
    setElapsedTime(0);
    setStartTime(Date.now());

    // Start mock simulation
    simulationService.start({
      onPhaseChange: (newPhase: Phase) => {
        setPhase(newPhase);
      },
      onMessage: (message: AgentMessage) => {
        setMessages((prev) => [...prev, message]);
      },
      onDecision: (dec: Decision) => {
        setDecision(dec);
      },
      onComplete: () => {
        setIsRunning(false);
      }
    });
  }, [shouldUseSSE, sessionId]);

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
    connectionStatus: shouldUseSSE ? sse.connectionStatus : undefined,
    error: shouldUseSSE ? sse.error : undefined,
    oauthRequest: shouldUseSSE ? sse.oauthRequest : undefined,
    startSimulation,
    resetSimulation,
    reconnect: shouldUseSSE ? sse.reconnect : undefined,
  };
};

