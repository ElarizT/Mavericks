import { apiService } from './apiService';
import { environment } from '@/lib/environment';
import { tokenService } from './apiService';
import { v4 as uuidv4 } from 'uuid';

export interface FileMetadata {
  id: string;
  session_id: string;
  request_id: string;
  original_name: string;
  mimetype: string;
  internal_id: string;
  internal_name: string;
  from_agent: boolean;
  created_at: string;
  size: number;
}

export interface FileData {
  file_id: string;
  session_id: string;
  request_id: string;
}

// File type validation
export const ALLOWED_FILE_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
  'application/pdf',
  'text/plain',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/csv',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
] as const;

export const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB

export function isValidFileType(file: File): boolean {
  return ALLOWED_FILE_TYPES.includes(
    file.type as (typeof ALLOWED_FILE_TYPES)[number]
  );
}

export function isValidFileSize(file: File): boolean {
  return file.size <= MAX_FILE_SIZE;
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

export function getFileIcon(file: File): string {
  const type = file.type;

  if (type.startsWith('image/')) return '🖼️';
  if (type === 'application/pdf') return '📄';
  if (type.startsWith('text/')) return '📝';
  if (type.includes('word') || type.includes('document')) return '📄';
  if (type.includes('sheet') || type.includes('excel')) return '📊';
  if (type.includes('csv')) return '📊';

  return '📎';
}

export const fileService = {
  async uploadFile(file: File, requestId?: string, sessionId?: string) {
    const formData = new FormData();
    formData.append('file', file);

    // Only add request_id and session_id if they are provided and are valid UUIDs
    // Otherwise, let the backend handle the file upload without these parameters
    if (requestId && sessionId) {
      // Generate proper UUIDs if the provided ones are not valid UUIDs
      const validRequestId = requestId.match(
        /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
      )
        ? requestId
        : uuidv4();
      const validSessionId = sessionId.match(
        /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
      )
        ? sessionId
        : uuidv4();

      formData.append('request_id', validRequestId);
      formData.append('session_id', validSessionId);
    }

    const response = await apiService.post<{ id: string }>('/files', formData, {
      noStringify: true,
      isFormData: true,
    });

    return response.data.id;
  },

  async downloadFile(fileId: string): Promise<{ url: string; fileId: string }> {
    if (typeof window === 'undefined') {
      throw new Error('Download not available in SSR environment');
    }

    const token = tokenService.getToken();
    const response = await fetch(`${environment.apiBaseUrl}/files/${fileId}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Get the blob
    const blob = await response.blob();

    // Create a download link
    const url = window.URL.createObjectURL(blob);

    return {
      url,
      fileId,
    };
  },

  async getFileMetadata(fileId: string) {
    const response = await apiService.get<FileMetadata>(
      `/files/${fileId}/metadata`
    );
    return response.data;
  },

  async getFilesBySessionId(sessionId: string) {
    const response = await apiService.get<FileData[]>('/files', {
      params: {
        session_id: sessionId,
      },
    });
    return response.data;
  },

  async getFileById(id: string) {
    const response = await apiService.get<unknown>(`/files/${id}`);
    return response.data;
  },
};

// Legacy function for backward compatibility
export async function uploadFile(
  file: File
): Promise<{ id: string; name: string }> {
  const fileId = await fileService.uploadFile(file);
  return {
    id: fileId,
    name: file.name,
  };
}
