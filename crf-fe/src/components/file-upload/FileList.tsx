import React from 'react';
import { FileUploadProgress } from './FileUploadProgress';

interface FileUpload {
  id: string;
  file: File;
  progress: number;
  status: 'uploading' | 'completed' | 'error';
  error?: string;
}

interface FileListProps {
  uploads: FileUpload[];
  onRemove?: (id: string) => void;
  className?: string;
}

export const FileList: React.FC<FileListProps> = ({
  uploads,
  onRemove,
  className = '',
}) => {
  if (uploads.length === 0) {
    return null;
  }

  return (
    <div className={`space-y-2 ${className}`}>
      {uploads.map((upload) => (
        <div key={upload.id} className='relative'>
          <FileUploadProgress
            fileName={upload.file.name}
            progress={upload.progress}
            status={upload.status}
            error={upload.error}
          />
          {onRemove && upload.status === 'completed' && (
            <button
              onClick={() => onRemove(upload.id)}
              className='absolute top-2 right-2 text-gray-400 hover:text-red-500 transition-colors'
            >
              ×
            </button>
          )}
        </div>
      ))}
    </div>
  );
};
