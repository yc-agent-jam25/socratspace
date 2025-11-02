/**
 * WebSocket hook for real-time updates
 * Currently in mock mode for frontend-only development
 */

import { useState } from 'react';

interface UseWebSocketReturn {
  lastMessage: MessageEvent | null;
  sendMessage: (message: string) => void;
  readyState: number;
}

/**
 * Mock WebSocket hook
 * Returns a mock connection state for development
 * Will be replaced with real WebSocket implementation when connecting to backend
 */
const useWebSocket = (_url: string): UseWebSocketReturn => {
  const [lastMessage] = useState<MessageEvent | null>(null);
  const [readyState] = useState<number>(WebSocket.OPEN); // Mock as always connected

  const sendMessage = (_message: string) => {
    // Mock implementation - does nothing
  };

  return { lastMessage, sendMessage, readyState };
};

export default useWebSocket;

// For future real implementation:
/*
import { useEffect, useState, useRef } from 'react';

const useWebSocket = (url: string): UseWebSocketReturn => {
  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CONNECTING);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      setReadyState(WebSocket.OPEN);
    };

    ws.current.onmessage = (event: MessageEvent) => {
      setLastMessage(event);
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.current.onclose = () => {
      setReadyState(WebSocket.CLOSED);
    };

    return () => {
      ws.current?.close();
    };
  }, [url]);

  const sendMessage = (message: string) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(message);
    }
  };

  return { lastMessage, sendMessage, readyState };
};
*/
