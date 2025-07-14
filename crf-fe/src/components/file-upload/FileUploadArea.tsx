import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface FileUploadAreaProps {
  onFilesSelected: (files: File[]) => void;
  accept?: string[];
  maxFiles?: number;
  className?: string;
}

export const FileUploadArea: React.FC<FileUploadAreaProps> = ({
  onFilesSelected,
  accept = ['.pdf', '.txt', '.doc', '.docx'],
  maxFiles = 5,
  className = '',
}) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      onFilesSelected(acceptedFiles);
    },
    [onFilesSelected]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: accept.reduce((acc, ext) => ({ ...acc, [ext]: [] }), {}),
    maxFiles,
  });

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
        ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }
        ${className}
      `}
    >
      <input {...getInputProps()} />
      <div className='space-y-2'>
        <div className='text-4xl mb-4'>📄</div>
        {isDragActive ? (
          <p className='text-blue-600 font-medium'>Drop the files here...</p>
        ) : (
          <>
            <p className='text-lg font-medium'>Upload Documents</p>
            <p className='text-gray-500 text-sm'>
              Drag and drop files here, or click to select files
            </p>
            <p className='text-gray-400 text-xs'>
              Supported formats: {accept.join(', ')}
            </p>
          </>
        )}
      </div>
    </div>
  );
};
