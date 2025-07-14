import { useState, useCallback } from 'react';
import { Message } from '@/types/chat';

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const addMessage = useCallback((message: Message) => {
    setMessages((prev) => [...prev, message]);
  }, []);

  const addUserMessage = useCallback(
    (content: string) => {
      const message: Message = {
        id: Date.now().toString(),
        content,
        role: 'user',
        timestamp: new Date().toISOString(),
      };
      addMessage(message);
    },
    [addMessage]
  );

  const addAssistantMessage = useCallback(
    (content: string) => {
      const message: Message = {
        id: Date.now().toString(),
        content,
        role: 'assistant',
        timestamp: new Date().toISOString(),
      };
      addMessage(message);
    },
    [addMessage]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    addMessage,
    addUserMessage,
    addAssistantMessage,
    clearMessages,
    isLoading,
    setIsLoading,
  };
};
