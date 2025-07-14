export interface Document {
  id: string;
  name: string;
  type: string;
  size: string;
  content?: string;
  summary?: string;
  uploadedAt: string;
  metadata?: {
    pageCount?: number;
    wordCount?: number;
    language?: string;
    tags?: string[];
  };
}

export interface DocumentUpload {
  id: string;
  file: File;
  progress: number;
  status: 'uploading' | 'completed' | 'error';
  error?: string;
}

export interface DocumentHighlight {
  start: number;
  end: number;
  color?: string;
  documentId: string;
}

export interface DocumentReference {
  documentId: string;
  documentName: string;
  highlights: DocumentHighlight[];
}
