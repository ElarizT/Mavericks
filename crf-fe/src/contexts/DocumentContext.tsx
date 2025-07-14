import { createContext, useContext } from 'react';
import { Document } from '@/types/document';

interface DocumentContextType {
  documents: Document[];
  addDocument: (document: Document) => void;
  removeDocument: (id: string) => void;
  selectedDocument: Document | null;
  setSelectedDocument: (document: Document | null) => void;
}

export const DocumentContext = createContext<DocumentContextType | undefined>(
  undefined
);

export const useDocument = () => {
  const context = useContext(DocumentContext);
  if (context === undefined) {
    throw new Error('useDocument must be used within a DocumentProvider');
  }
  return context;
};
