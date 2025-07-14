'use client';
import { useState, useRef } from 'react';
import { Paperclip, X, Send, Upload, AlertCircle } from 'lucide-react';
import {
  getFileIcon,
  formatFileSize,
  isValidFileType,
  isValidFileSize,
} from '@/services/fileUploadService';

interface UploadResult {
  id: string;
  name: string;
}

interface ChatInputProps {
  onSendMessage: (message: string, fileIds?: string[]) => void;
  onFileUpload?: (file: File) => Promise<UploadResult>;
  disabled?: boolean;
  placeholder?: string;
  isUploading?: boolean;
  fullScreen?: boolean;
}

interface AttachedFile {
  clientId: string;
  file: File;
  preview?: string;
  id?: string;
  loading: boolean;
  error?: string;
}

export const ChatInput = ({
  onSendMessage,
  onFileUpload,
  disabled = false,
  placeholder = 'Type your message...',
  isUploading = false,
}: ChatInputProps) => {
  const [input, setInput] = useState('');
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Get successfully uploaded file IDs
    const fileIds = attachedFiles
      .filter((file) => !file.loading && file.id && !file.error)
      .map((file) => file.id!);

    if ((input.trim() || fileIds.length > 0) && !disabled) {
      onSendMessage(input.trim(), fileIds);
      setInput('');

      // Remove successfully sent files, keep failed ones for retry
      setAttachedFiles((prev) =>
        prev.filter((file) => file.loading || file.error)
      );
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);

    if (!onFileUpload) {
      console.warn('No file upload handler provided');
      return;
    }

    // Filter valid files
    const validFiles = files.filter((file) => {
      if (!isValidFileType(file)) {
        console.warn(`Invalid file type: ${file.type}`);
        return false;
      }
      if (!isValidFileSize(file)) {
        console.warn(`File too large: ${file.size} bytes`);
        return false;
      }
      return true;
    });

    // Create placeholders immediately for UI feedback
    const newAttachedFiles: AttachedFile[] = validFiles.map((file) => {
      const clientId = `${Date.now()}-${file.name}`;
      const attachedFile: AttachedFile = {
        clientId,
        file,
        loading: true,
      };

      // Create preview for images
      if (file.type.startsWith('image/')) {
        attachedFile.preview = URL.createObjectURL(file);
      }

      return attachedFile;
    });

    setAttachedFiles((prev) => [...prev, ...newAttachedFiles]);

    // Upload files using the provided callback
    for (const attachedFile of newAttachedFiles) {
      try {
        const uploadResult = await onFileUpload(attachedFile.file);

        // Update with real file ID from backend
        setAttachedFiles((prev) =>
          prev.map((file) =>
            file.clientId === attachedFile.clientId
              ? { ...file, id: uploadResult.id, loading: false }
              : file
          )
        );
      } catch (error) {
        // Mark file as failed
        setAttachedFiles((prev) =>
          prev.map((file) =>
            file.clientId === attachedFile.clientId
              ? {
                  ...file,
                  loading: false,
                  error:
                    error instanceof Error ? error.message : 'Upload failed',
                }
              : file
          )
        );
        console.error('File upload failed:', error);
      }
    }

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeFile = (clientId: string) => {
    setAttachedFiles((prev) => {
      const fileToRemove = prev.find((file) => file.clientId === clientId);
      // Revoke object URL to prevent memory leaks
      if (fileToRemove?.preview) {
        URL.revokeObjectURL(fileToRemove.preview);
      }
      return prev.filter((file) => file.clientId !== clientId);
    });
  };

  const retryUpload = async (clientId: string) => {
    if (!onFileUpload) return;

    const fileToRetry = attachedFiles.find(
      (file) => file.clientId === clientId
    );
    if (!fileToRetry || fileToRetry.loading || fileToRetry.id) return;

    // Set loading state
    setAttachedFiles((prev) =>
      prev.map((file) =>
        file.clientId === clientId
          ? { ...file, loading: true, error: undefined }
          : file
      )
    );

    try {
      const uploadResult = await onFileUpload(fileToRetry.file);

      // Update with real file ID
      setAttachedFiles((prev) =>
        prev.map((file) =>
          file.clientId === clientId
            ? { ...file, id: uploadResult.id, loading: false }
            : file
        )
      );
    } catch (error) {
      // Mark as failed again
      setAttachedFiles((prev) =>
        prev.map((file) =>
          file.clientId === clientId
            ? {
                ...file,
                loading: false,
                error: error instanceof Error ? error.message : 'Upload failed',
              }
            : file
        )
      );
      console.error('File upload retry failed:', error);
    }
  };

  return (
    <div className='w-full px-4 py-4 bg-white border-t border-gray-100'>
      {/* Attached Files Display */}
      {attachedFiles.length > 0 && (
        <div className='mb-3 p-3 bg-gray-50 rounded-lg'>
          <div className='flex flex-wrap gap-2'>
            {attachedFiles.map((attachedFile) => (
              <div
                key={attachedFile.clientId}
                className={`flex items-center gap-2 p-2 rounded-lg border ${
                  attachedFile.error
                    ? 'bg-red-50 border-red-200'
                    : attachedFile.loading
                    ? 'bg-blue-50 border-blue-200'
                    : 'bg-white border-gray-200'
                }`}
              >
                <span className='text-lg'>
                  {getFileIcon(attachedFile.file)}
                </span>
                <div className='flex flex-col min-w-0'>
                  <span className='text-sm font-medium truncate max-w-[150px]'>
                    {attachedFile.file.name}
                  </span>
                  <span className='text-xs text-gray-500'>
                    {formatFileSize(attachedFile.file.size)}
                  </span>
                </div>
                {attachedFile.loading && (
                  <div className='flex items-center gap-1'>
                    <div className='w-3 h-3 border-2 border-blue-500 border-t-transparent rounded-full animate-spin'></div>
                    <span className='text-xs text-blue-600'>Uploading...</span>
                  </div>
                )}
                {attachedFile.error && (
                  <div className='flex items-center gap-1'>
                    <AlertCircle className='w-3 h-3 text-red-500' />
                    <span className='text-xs text-red-600'>Failed</span>
                  </div>
                )}
                <button
                  type='button'
                  onClick={() => removeFile(attachedFile.clientId)}
                  className='ml-2 p-1 text-gray-400 hover:text-red-500 transition-colors'
                  title='Remove file'
                >
                  <X className='w-3 h-3' />
                </button>
                {attachedFile.error && (
                  <button
                    type='button'
                    onClick={() => retryUpload(attachedFile.clientId)}
                    className='ml-1 p-1 text-gray-400 hover:text-blue-500 transition-colors'
                    title='Retry upload'
                  >
                    <Upload className='w-3 h-3' />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
      <form
        onSubmit={handleSubmit}
        className='flex items-center w-full max-w-full'
        style={{ margin: 0 }}
      >
        <div className='flex-1 flex items-center'>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={placeholder}
            disabled={disabled || isUploading}
            rows={1}
            className='w-full h-14 px-4 py-0 border-2 border-blue-400 focus:border-blue-500 rounded-2xl outline-none text-lg transition-all duration-200 bg-white placeholder-gray-400 resize-none hide-scrollbar align-middle'
            style={{
              minHeight: '56px',
              maxHeight: '120px',
              overflow: 'hidden',
              lineHeight: '56px',
            }}
            autoComplete='off'
            onInput={(e) => {
              const target = e.target as HTMLTextAreaElement;
              target.style.height = '56px';
              target.style.height = Math.min(target.scrollHeight, 120) + 'px';
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (!disabled && !isUploading && input.trim()) {
                  handleSubmit(e as React.FormEvent);
                }
              }
            }}
          />
        </div>
        <input
          ref={fileInputRef}
          type='file'
          multiple
          accept='image/*,.pdf,.txt,.doc,.docx'
          onChange={handleFileSelect}
          className='hidden'
        />
        <button
          type='button'
          onClick={() => fileInputRef.current?.click()}
          disabled={disabled || isUploading}
          className='ml-3 w-12 h-12 flex items-center justify-center bg-white border-2 border-blue-400 text-blue-500 hover:bg-blue-50 hover:border-blue-500 rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'
          style={{ minWidth: '48px', minHeight: '48px' }}
          title='Attach files'
        >
          <Paperclip size={22} />
        </button>
        <button
          type='submit'
          disabled={disabled || isUploading || !input.trim()}
          className='ml-3 w-12 h-12 flex items-center justify-center bg-blue-500 hover:bg-blue-600 text-white rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'
          style={{ minWidth: '48px', minHeight: '48px' }}
        >
          <Send size={24} />
        </button>
      </form>
    </div>
  );
};
