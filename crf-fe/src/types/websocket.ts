export interface WebSocketMessage {
  type: string;
  payload: unknown;
  timestamp: string;
  id?: string;
}

export interface ChatMessage extends WebSocketMessage {
  type: 'chat_message';
  payload: {
    content: string;
    role: 'user' | 'assistant';
    documentReferences?: Array<{
      documentId: string;
      documentName: string;
      highlights: Array<{
        start: number;
        end: number;
        color?: string;
      }>;
    }>;
  };
}

export interface DocumentUploadMessage extends WebSocketMessage {
  type: 'document_upload';
  payload: {
    documentId: string;
    status: 'processing' | 'completed' | 'error';
    progress?: number;
    error?: string;
  };
}

export interface ConnectionStatusMessage extends WebSocketMessage {
  type: 'connection_status';
  payload: {
    status: 'connected' | 'disconnected' | 'reconnecting';
    timestamp: string;
  };
}

export interface ErrorMessage extends WebSocketMessage {
  type: 'error';
  payload: {
    code: string;
    message: string;
    details?: unknown;
  };
}

export type WebSocketEventMap = {
  chat_message: ChatMessage;
  document_upload: DocumentUploadMessage;
  connection_status: ConnectionStatusMessage;
  error: ErrorMessage;
};

export interface WebSocketState {
  isConnected: boolean;
  error: string | null;
  lastMessage?: WebSocketMessage;
}
