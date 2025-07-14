'use client';
import { useState, useEffect } from 'react';
import { authService } from '@/services/authService';
import { websocketManager } from '@/services/websocketService';
import { fileService } from '@/services/fileUploadService';
import { modelService } from '@/services/modelService';
import { v4 as uuidv4 } from 'uuid';
import { ChatDisplay } from './ChatDisplay';
import { ChatInput } from './ChatInput';
import { TypingIndicator } from './TypingIndicator';
import { Message } from '@/types/chat';

interface UploadResult {
  id: string;
  name: string;
}

// Add prop for force enabling input and full screen mode
export function ChatContainer({
  forceEnableInput = false,
  fullScreen = false,
}: {
  forceEnableInput?: boolean;
  fullScreen?: boolean;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [isUploading, setIsUploading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [modelConfig, setModelConfig] = useState<{
    provider: string;
    configs: Array<{ name: string }>;
  } | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<
    'disconnected' | 'connecting' | 'connected'
  >('disconnected');

  useEffect(() => {
    let isMounted = true;

    const autoLoginAndConnect = async () => {
      try {
        console.log('Starting authentication and WebSocket connection...');

        // Check if user is already authenticated
        let user = authService.getCurrentUser();
        console.log('Current user from storage:', user);
        const username = process.env.NEXT_PUBLIC_AUTH_USERNAME;
        const password = process.env.NEXT_PUBLIC_AUTH_PASSWORD;
        if (!user) {
          console.log('No user found, attempting auto-login...');
          // Input your credentials for AgentOS - change to your own credentials
          if (username && password) {
            user = await authService.login(username, password);
            console.log('Auto-login successful:', user);
          } else {
            console.log('Auto-login failed: missing credentials');
          }
        }

        // If we have a user (either from storage or after auto-login), connect
        if (user && isMounted) {
          console.log('User authenticated, setting up WebSocket connection...');
          setIsAuthenticated(true);
          setConnectionStatus('connecting');

          // Generate session ID for this chat session
          const chatSessionId = `session_${Date.now()}`;
          setSessionId(chatSessionId);
          console.log('Generated session ID:', chatSessionId);

          // Connect to WebSocket using your original API
          await websocketManager.connect();
          console.log('WebSocket connection initiated');
          if (isMounted) {
            setConnectionStatus('connected');
          }

          // Set up message handler using your original API
          websocketManager.onMessage((newMessage: unknown) => {
            console.log('Received message:', newMessage);

            // Handle different message types
            const message = newMessage as {
              type?: string;
              [key: string]: unknown;
            };
            if (message.type === 'agent_log') {
              // Skip log messages
              return;
            }

            // Add all messages to the array - let the display component handle the rendering
            if (isMounted) {
              setMessages((prevMessages) => [
                ...prevMessages,
                message as Message,
              ]);
              setIsTyping(false);
            }
          });

          const fetchModel = async () => {
            try {
              console.log('Fetching model configurations...');
              const models = await modelService.getModels();
              console.log('Fetched model configurations:', models);
              if (models && models.length > 0) {
                const firstModel = models[0];
                if (isMounted) {
                  setModelConfig(firstModel);
                }
                console.log('Set model config:', firstModel);
              }
            } catch (error) {
              console.error('Error fetching model configurations:', error);
            }
          };

          await fetchModel();
        }
      } catch (error) {
        console.error('Error during authentication/connection:', error);
        if (isMounted) {
          setConnectionStatus('disconnected');
        }
      }
    };

    autoLoginAndConnect();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleFileUpload = async (file: File): Promise<UploadResult> => {
    setIsUploading(true);
    try {
      // Generate proper UUIDs for request_id and session_id
      const requestId = uuidv4();
      const fileSessionId = uuidv4();

      // Upload the file using the file service
      const uploadResult = await fileService.uploadFile(
        file,
        requestId,
        fileSessionId
      );
      console.log('File uploaded successfully:', uploadResult);

      return {
        id: uploadResult,
        name: file.name,
      };
    } catch (error) {
      console.error('File upload failed:', error);
      throw error;
    } finally {
      setIsUploading(false);
    }
  };

  const handleSendMessage = async (input: string, fileIds?: string[]) => {
    if (!modelConfig) {
      console.error('No model configuration available');
      return;
    }

    if (!sessionId) {
      console.error('No session ID available');
      return;
    }

    try {
      // Show typing indicator
      setIsTyping(true);

      // Create user message
      const userMessage: Message = {
        type: 'user_message',
        data: input,
        files:
          fileIds?.map((id) => ({
            id,
            name: '',
            original_name: '',
            size: 0,
          })) || [],
      };

      // Add user message to display
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      // Send message via WebSocket (original simple structure)
      const wsMessage = {
        message: input,
        llm_name: modelConfig.configs?.[0]?.name,
        provider: modelConfig.provider,
        ...(fileIds && fileIds.length > 0 && { files: fileIds }),
      };

      console.log('Sending message via WebSocket:', wsMessage);
      console.log('Files being sent:', fileIds);
      websocketManager.sendMessage(wsMessage);
    } catch (error) {
      console.error('Error sending message:', error);
      setIsTyping(false);
    }
  };

  return (
    <div className={`flex flex-col h-full ${fullScreen ? 'bg-white' : ''}`}>
      {/* Connection Status Bar removed for clean UI */}
      {/* Chat Display */}
      <div className='flex-1 relative'>
        <ChatDisplay messages={messages} />
        {isTyping && <TypingIndicator />}
      </div>

      {/* Chat Input */}
      <ChatInput
        onSendMessage={handleSendMessage}
        onFileUpload={handleFileUpload}
        disabled={
          forceEnableInput
            ? false
            : !isAuthenticated || connectionStatus !== 'connected'
        }
        isUploading={isUploading}
        placeholder={
          !isAuthenticated
            ? 'Authenticating...'
            : connectionStatus !== 'connected'
            ? 'Connecting to server...'
            : 'Type your message or upload a document...'
        }
        fullScreen={fullScreen}
      />
    </div>
  );
}
