import React from 'react';
import { DocumentSummary } from './DocumentSummary';
import { Document } from '@/types/document';

interface DocumentPaneProps {
  documents: Document[];
  selectedDocument?: Document;
  onSelectDocument: (document: Document) => void;
  className?: string;
}

export const DocumentPane: React.FC<DocumentPaneProps> = ({
  documents,
  selectedDocument,
  onSelectDocument,
  className = '',
}) => {
  return (
    <div className={`flex flex-col h-full ${className}`}>
      <div className='p-4 border-b'>
        <h3 className='text-lg font-semibold'>Documents</h3>
      </div>

      <div className='flex-1 overflow-y-auto'>
        {documents.length === 0 ? (
          <div className='p-4 text-center text-gray-500'>
            No documents uploaded yet
          </div>
        ) : (
          <div className='p-4 space-y-2'>
            {documents.map((document) => (
              <div
                key={document.id}
                className={`p-3 rounded-lg cursor-pointer transition-colors ${
                  selectedDocument?.id === document.id
                    ? 'bg-blue-100 border-blue-300'
                    : 'bg-gray-50 hover:bg-gray-100'
                }`}
                onClick={() => onSelectDocument(document)}
              >
                <h4 className='font-medium text-sm'>{document.name}</h4>
                <p className='text-xs text-gray-500 mt-1'>
                  {document.size} • {document.type}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedDocument && (
        <div className='border-t'>
          <DocumentSummary document={selectedDocument} />
        </div>
      )}
    </div>
  );
};
