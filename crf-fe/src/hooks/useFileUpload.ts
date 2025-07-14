import { useState, useCallback } from 'react';

interface FileUpload {
  id: string;
  file: File;
  progress: number;
  status: 'uploading' | 'completed' | 'error';
  error?: string;
}

export const useFileUpload = () => {
  const [uploads, setUploads] = useState<FileUpload[]>([]);

  const addUpload = useCallback((file: File) => {
    const upload: FileUpload = {
      id: Date.now().toString(),
      file,
      progress: 0,
      status: 'uploading',
    };
    setUploads((prev) => [...prev, upload]);
    return upload.id;
  }, []);

  const updateUpload = useCallback(
    (id: string, updates: Partial<FileUpload>) => {
      setUploads((prev) =>
        prev.map((upload) =>
          upload.id === id ? { ...upload, ...updates } : upload
        )
      );
    },
    []
  );

  const removeUpload = useCallback((id: string) => {
    setUploads((prev) => prev.filter((upload) => upload.id !== id));
  }, []);

  const clearUploads = useCallback(() => {
    setUploads([]);
  }, []);

  return {
    uploads,
    addUpload,
    updateUpload,
    removeUpload,
    clearUploads,
  };
};
