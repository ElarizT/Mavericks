export interface Message {
  id?: string;
  content?: string;
  role?: 'user' | 'assistant' | 'system';
  timestamp?: string;
  type?: string;
  response?: {
    response?: {
      response?: string;
    };
  };
  data?: string; // For raw_text messages
  files?: Array<{
    id: string;
    name: string;
    size: number;
    original_name?: string;
  }>;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
  updatedAt: string;
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

export interface ChatResponse {
  message: string;
  documentReferences?: Array<{
    documentId: string;
    documentName: string;
    highlights: Array<{
      start: number;
      end: number;
      color?: string;
    }>;
  }>;
}
