import React from 'react';

interface FileUploadProgressProps {
  fileName: string;
  progress: number;
  status: 'uploading' | 'completed' | 'error';
  error?: string;
  className?: string;
}

export const FileUploadProgress: React.FC<FileUploadProgressProps> = ({
  fileName,
  progress,
  status,
  error,
  className = '',
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'completed':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-blue-500';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'completed':
        return 'Uploaded';
      case 'error':
        return 'Failed';
      default:
        return 'Uploading...';
    }
  };

  return (
    <div className={`p-3 border rounded-lg ${className}`}>
      <div className='flex items-center justify-between mb-2'>
        <span className='text-sm font-medium truncate'>{fileName}</span>
        <span
          className={`text-xs px-2 py-1 rounded ${
            status === 'completed'
              ? 'bg-green-100 text-green-800'
              : status === 'error'
              ? 'bg-red-100 text-red-800'
              : 'bg-blue-100 text-blue-800'
          }`}
        >
          {getStatusText()}
        </span>
      </div>

      <div className='w-full bg-gray-200 rounded-full h-2'>
        <div
          className={`h-2 rounded-full transition-all duration-300 ${getStatusColor()}`}
          style={{ width: `${progress}%` }}
        />
      </div>

      {error && <p className='text-xs text-red-600 mt-1'>{error}</p>}
    </div>
  );
};
