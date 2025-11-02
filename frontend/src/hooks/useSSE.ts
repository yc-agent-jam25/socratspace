/**
 * Server-Side Events (SSE) hook for real-time updates
 * Replaces WebSocket with simpler SSE implementation
 */

import { useEffect, useState, useRef, useCallback } from 'react';
import type { Phase, AgentMessage, Decision } from '../lib/types';

interface UseSSEReturn {
  phase: Phase;
  messages: AgentMessage[];
  decision: Decision | null;
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error';
  error: string | null;
  reconnect: () => void;
}

interface SSEMessage {
  type: 'phase_change' | 'agent_message' | 'decision' | 'error' | 'ping';
  data: any;
}

/**
 * SSE Hook for real-time updates from backend
 * 
 * @param sessionId - Session ID to connect to
 * @param enabled - Whether to enable SSE connection (default: true)
 */
export const useSSE = (sessionId: string | null, enabled: boolean = true): UseSSEReturn => {
  const [phase, setPhase] = useState<Phase>('idle');
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const [decision, setDecision] = useState<Decision | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
  const [error, setError] = useState<string | null>(null);
  
  const eventSourceRef = useRef<EventSource | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const reconnectAttemptsRef = useRef<number>(0);
  const isCompletedRef = useRef<boolean>(false); // Track if stream completed successfully
  
  const MAX_RECONNECT_ATTEMPTS = 5;
  const RECONNECT_DELAY = 1000; // Start with 1 second

  const connect = useCallback(() => {
    if (!sessionId || !enabled) {
      return;
    }

    // Close existing connection if any
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    // Clear any pending reconnection
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const sseUrl = `${API_URL}/api/sse/${sessionId}`;

    setConnectionStatus('connecting');
    setError(null);

    try {
      console.log('Attempting SSE connection to:', sseUrl);
      
      // EventSource with error handling
      const eventSource = new EventSource(sseUrl, {
        // Note: EventSource doesn't support custom headers, so we rely on CORS
      });
      
      eventSourceRef.current = eventSource;

      eventSource.onopen = () => {
        console.log('SSE connection opened for session:', sessionId);
        setConnectionStatus('connected');
        reconnectAttemptsRef.current = 0; // Reset on successful connection
      };

      eventSource.onmessage = (event: MessageEvent) => {
        try {
          const sseMessage: SSEMessage = JSON.parse(event.data);
          
          switch (sseMessage.type) {
            case 'phase_change':
              const newPhase = sseMessage.data.phase as Phase;
              setPhase(newPhase);
              // Mark as completed when phase is 'completed'
              if (newPhase === 'completed') {
                isCompletedRef.current = true;
              }
              break;
            
            case 'agent_message':
              const agentMessage: AgentMessage = {
                agent: sseMessage.data.agent,
                message: sseMessage.data.message,
                message_type: sseMessage.data.message_type || 'info',
                timestamp: sseMessage.data.timestamp || Date.now(),
              };
              setMessages((prev) => {
                // Avoid duplicates by checking timestamp + agent + message hash
                const exists = prev.some(
                  (m) => m.agent === agentMessage.agent &&
                    m.message === agentMessage.message &&
                    m.timestamp === agentMessage.timestamp
                );
                if (exists) return prev;
                return [...prev, agentMessage].sort((a, b) => a.timestamp - b.timestamp);
              });
              break;
            
            case 'decision':
              setDecision(sseMessage.data as Decision);
              setPhase('completed');
              isCompletedRef.current = true; // Mark as completed
              break;
            
            case 'error':
              setError(sseMessage.data.message || 'An error occurred');
              setConnectionStatus('error');
              break;
            
            case 'ping':
              // Heartbeat - just acknowledge, no action needed
              break;
            
            default:
              console.warn('Unknown SSE message type:', sseMessage.type);
          }
        } catch (parseError) {
          console.error('Error parsing SSE message:', parseError, event.data);
        }
      };

      eventSource.onerror = (error: Event) => {
        const eventSource = eventSourceRef.current;
        
        // If stream completed successfully, don't treat closure as error
        if (isCompletedRef.current && eventSource?.readyState === EventSource.CLOSED) {
          console.log('SSE stream completed successfully, connection closed normally');
          setConnectionStatus('disconnected');
          // Close connection cleanly
          if (eventSourceRef.current) {
            eventSourceRef.current.close();
            eventSourceRef.current = null;
          }
          return;
        }
        
        console.error('SSE connection error:', error);
        console.error('EventSource state:', eventSource?.readyState);
        console.error('EventSource URL:', eventSource?.url);
        
        // Log readyState details
        // 0 = CONNECTING, 1 = OPEN, 2 = CLOSED
        if (eventSource) {
          const states = ['CONNECTING', 'OPEN', 'CLOSED'];
          console.error('EventSource readyState:', states[eventSource.readyState] || 'UNKNOWN');
        }
        
        // Only set error status if not completed
        if (!isCompletedRef.current) {
          setConnectionStatus('error');
          setError('Connection error. Attempting to reconnect...');
        }
        
        // Close current connection
        if (eventSourceRef.current) {
          eventSourceRef.current.close();
          eventSourceRef.current = null;
        }

        // Only attempt reconnection if stream didn't complete successfully
        if (!isCompletedRef.current && reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
          reconnectAttemptsRef.current += 1;
          const delay = RECONNECT_DELAY * reconnectAttemptsRef.current;
          
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log(`Reconnecting SSE (attempt ${reconnectAttemptsRef.current}/${MAX_RECONNECT_ATTEMPTS})...`);
            connect();
          }, delay);
        } else if (!isCompletedRef.current) {
          setError('Connection failed after multiple attempts. Please refresh the page.');
          setConnectionStatus('disconnected');
        }
      };
    } catch (err) {
      console.error('Failed to create SSE connection:', err);
      setConnectionStatus('error');
      setError(err instanceof Error ? err.message : 'Failed to connect');
    }
  }, [sessionId, enabled]);

  const disconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    setConnectionStatus('disconnected');
    isCompletedRef.current = false; // Reset completion flag
  }, []);

  const reconnect = useCallback(() => {
    reconnectAttemptsRef.current = 0; // Reset attempts
    disconnect();
    setTimeout(connect, 100);
  }, [connect, disconnect]);

  // Connect on mount or when sessionId/enabled changes
  useEffect(() => {
    // Reset completion flag when starting new connection
    isCompletedRef.current = false;
    
    if (sessionId && enabled) {
      connect();
    } else {
      disconnect();
    }

    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, [sessionId, enabled, connect, disconnect]);

  return {
    phase,
    messages,
    decision,
    connectionStatus,
    error,
    reconnect,
  };
};

export default useSSE;

