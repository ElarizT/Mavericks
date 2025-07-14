import { apiService } from './apiService';

export interface IChat {
  session_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ChatHistory {
  total_count: number;
  items: {
    content: string;
    sender_type: string;
    created_at: string;
    request_id: string;
  }[];
}

export interface AttachedFile {
  id: string;
  name: string;
}

export const chatService = {
  async getChatsList(params?: { offset?: string; limit?: string }) {
    const response = await apiService.get<{ chats: IChat[] }>('/api/chats', {
      params,
    });
    return response.data;
  },

  async getChatHistory(params: {
    session_id: string;
    page?: string;
    per_page?: string;
    user_id?: string;
  }) {
    const response = await apiService.get<ChatHistory>('/api/chat', { params });
    return response.data;
  },

  async createChat(id: string) {
    const response = await apiService.post('/api/chats', {
      session_id: id,
    });
    return response.data;
  },

  async updateChat(id: string, title: string) {
    await apiService.patch<IChat>(
      '/api/chat',
      { title },
      { params: { session_id: id } }
    );
  },

  async deleteChat(id: string) {
    await apiService.delete('/api/chat', { params: { session_id: id } });
  },
};
