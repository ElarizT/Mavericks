import React from 'react';
import { WebSocketProvider } from './WebSocketProvider';
import { ChatProvider } from './ChatProvider';

interface ProvidersProps {
  children: React.ReactNode;
  websocketUrl?: string;
}

export const Providers: React.FC<ProvidersProps> = ({
  children,
  websocketUrl,
}) => {
  return (
    <WebSocketProvider url={websocketUrl}>
      <ChatProvider>{children}</ChatProvider>
    </WebSocketProvider>
  );
};
