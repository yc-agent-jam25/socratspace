/**
 * WebSocket hook for real-time updates
 * TODO: Implement WebSocket connection management
 */

import { useEffect, useState, useRef } from 'react';

interface UseWebSocketReturn {
  lastMessage: MessageEvent | null;
  sendMessage: (message: string) => void;
  readyState: number;
}

const useWebSocket = (url: string): UseWebSocketReturn => {
  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CONNECTING);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // TODO: Create WebSocket connection
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
      setReadyState(WebSocket.OPEN);
    };

    ws.current.onmessage = (event: MessageEvent) => {
      setLastMessage(event);
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
      setReadyState(WebSocket.CLOSED);
    };

    // Cleanup on unmount
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

export default useWebSocket;
