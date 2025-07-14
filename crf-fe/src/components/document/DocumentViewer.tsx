import React from 'react';
import { Document } from '@/types/document';

interface DocumentViewerProps {
  document: Document;
  className?: string;
}

export const DocumentViewer: React.FC<DocumentViewerProps> = ({
  document,
  className = '',
}) => {
  return (
    <div className={`h-full overflow-y-auto ${className}`}>
      <div className='p-4'>
        <h3 className='text-lg font-semibold mb-4'>{document.name}</h3>

        {document.content ? (
          <div className='prose max-w-none'>
            <pre className='whitespace-pre-wrap text-sm bg-gray-50 p-4 rounded'>
              {document.content}
            </pre>
          </div>
        ) : (
          <div className='text-center text-gray-500 py-8'>
            <p>Document content not available</p>
          </div>
        )}
      </div>
    </div>
  );
};
