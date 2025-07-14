import React from 'react';
import { Document } from '@/types/document';

interface DocumentSummaryProps {
  document: Document;
  className?: string;
}

export const DocumentSummary: React.FC<DocumentSummaryProps> = ({
  document,
  className = '',
}) => {
  return (
    <div className={`p-4 ${className}`}>
      <h4 className='font-medium text-sm mb-2'>Document Summary</h4>
      <div className='space-y-2 text-xs text-gray-600'>
        <div className='flex justify-between'>
          <span>Name:</span>
          <span className='font-medium'>{document.name}</span>
        </div>
        <div className='flex justify-between'>
          <span>Type:</span>
          <span>{document.type}</span>
        </div>
        <div className='flex justify-between'>
          <span>Size:</span>
          <span>{document.size}</span>
        </div>
        <div className='flex justify-between'>
          <span>Uploaded:</span>
          <span>{new Date(document.uploadedAt).toLocaleDateString()}</span>
        </div>
        {document.summary && (
          <div className='mt-3 pt-3 border-t'>
            <div className='font-medium mb-1'>Summary:</div>
            <p className='text-gray-700'>{document.summary}</p>
          </div>
        )}
      </div>
    </div>
  );
};
