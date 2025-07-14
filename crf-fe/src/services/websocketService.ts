import { tokenService } from './apiService';

const WEBSOCKET_URL = 'ws://localhost:8000/frontend/ws';

export interface UserMessage {
  message: string;
  provider?: string;
  llm_name?: string;
  files?: string[];
}

export interface FrontendMessage extends UserMessage {
  provider: string;
  llm_name: string;
}

class WebSocketManager {
  private socket: WebSocket | null = null;
  private messageHandler: ((message: unknown) => void) | null = null;

  async connect() {
    const token = tokenService.getToken();
    if (!token) {
      console.error('Authentication token not found. Please log in.');
      return;
    }

    // Close any existing connection before creating a new one
    if (this.socket) {
      this.socket.close();
    }

    // Create the WebSocket instance with the token as a query parameter
    this.socket = new WebSocket(`${WEBSOCKET_URL}?token=${token}`);

    this.socket.onopen = () => {
      console.log('WebSocket connection established.');
    };

    this.socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        console.log('Received JSON message:', message);
        // If a message handler is set, call it with the new message
        if (this.messageHandler) {
          this.messageHandler(message);
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message as JSON:', event.data);
        console.error('Parse error:', error);
        // Optionally, you can handle plain text messages here
        if (this.messageHandler) {
          this.messageHandler({ type: 'raw_text', data: event.data });
        }
      }
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed.');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  // Method for UI components to subscribe to messages
  onMessage(handler: (message: unknown) => void) {
    this.messageHandler = handler;
  }

  // Method to send a message to the server - accepts any object with at least a message field
  sendMessage(message: UserMessage) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log('Sending message payload:', message);
      this.socket.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected.');
    }
  }
}

// Export a single instance (singleton pattern)
export const websocketManager = new WebSocketManager();
