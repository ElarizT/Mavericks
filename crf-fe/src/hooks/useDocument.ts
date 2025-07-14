import { useState, useCallback } from 'react';
import { Document } from '@/types/document';

export const useDocument = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(
    null
  );

  const addDocument = useCallback((document: Document) => {
    setDocuments((prev) => [...prev, document]);
  }, []);

  const removeDocument = useCallback(
    (id: string) => {
      setDocuments((prev) => prev.filter((doc) => doc.id !== id));
      if (selectedDocument?.id === id) {
        setSelectedDocument(null);
      }
    },
    [selectedDocument]
  );

  const updateDocument = useCallback(
    (id: string, updates: Partial<Document>) => {
      setDocuments((prev) =>
        prev.map((doc) => (doc.id === id ? { ...doc, ...updates } : doc))
      );
      if (selectedDocument?.id === id) {
        setSelectedDocument((prev) => (prev ? { ...prev, ...updates } : null));
      }
    },
    [selectedDocument]
  );

  const clearDocuments = useCallback(() => {
    setDocuments([]);
    setSelectedDocument(null);
  }, []);

  return {
    documents,
    selectedDocument,
    setSelectedDocument,
    addDocument,
    removeDocument,
    updateDocument,
    clearDocuments,
  };
};
