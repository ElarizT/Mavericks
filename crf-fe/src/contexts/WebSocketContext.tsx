import { createContext, useContext } from 'react';

interface WebSocketContextType {
  socket: WebSocket | null;
  isConnected: boolean;
  error: string | null;
  sendMessage: (message: unknown) => void;
}

export const WebSocketContext = createContext<WebSocketContextType | undefined>(
  undefined
);

export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (context === undefined) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};
