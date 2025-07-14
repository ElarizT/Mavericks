import { Message } from '@/types/chat';
import { Bot, User, FileText, Image as ImageIcon, File } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import styles from './ChatDisplay.module.css';

interface ChatDisplayProps {
  messages: Message[];
}

export const ChatDisplay = ({ messages }: ChatDisplayProps) => {
  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase() || '';
    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension)) {
      return <ImageIcon className='w-4 h-4' />;
    }
    if (['pdf'].includes(extension)) {
      return <FileText className='w-4 h-4' />;
    }
    return <File className='w-4 h-4' />;
  };

  return (
    <div className='flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 sm:space-y-6 bg-gradient-to-b from-gray-50 to-white'>
      {messages.length === 0 ? (
        <div className='flex flex-col items-center justify-center h-full text-center'>
          <div className='w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mb-3 sm:mb-4'>
            <Bot className='w-7 h-7 sm:w-8 sm:h-8 text-white' />
          </div>
          <h3 className='text-lg sm:text-xl font-semibold text-gray-900 mb-1 sm:mb-2'>
            Welcome to LawCo AI Assistant
          </h3>
          <p className='text-gray-600 max-w-md leading-relaxed text-sm sm:text-base mb-4'>
            I&apos;m here to help you with legal questions, document analysis,
            and professional guidance. Start by typing a message or uploading a
            document.
          </p>
          <div className='mt-2 flex flex-wrap gap-2 justify-center'>
            <div className='px-2 py-1 sm:px-3 sm:py-1 bg-blue-100 text-blue-800 rounded-full text-xs sm:text-sm'>
              &quot;Analyze this contract&quot;
            </div>
            <div className='px-2 py-1 sm:px-3 sm:py-1 bg-purple-100 text-purple-800 rounded-full text-xs sm:text-sm'>
              &quot;Legal advice needed&quot;
            </div>
            <div className='px-2 py-1 sm:px-3 sm:py-1 bg-green-100 text-green-800 rounded-full text-xs sm:text-sm'>
              &quot;Document review&quot;
            </div>
          </div>
        </div>
      ) : (
        messages.map((msg, index) => {
          const isUser = msg.type === 'user_message';

          return (
            <div
              key={index}
              className={`flex items-start space-x-2 sm:space-x-3 chat-message ${
                isUser ? 'flex-row-reverse space-x-reverse user' : 'bot'
              }`}
            >
              {/* Avatar */}
              <div
                className={`flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-full flex items-center justify-center ${
                  isUser
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600'
                    : 'bg-gradient-to-r from-gray-600 to-gray-700'
                }`}
              >
                {isUser ? (
                  <User className='w-4 h-4 sm:w-5 sm:h-5 text-white' />
                ) : (
                  <Bot className='w-4 h-4 sm:w-5 sm:h-5 text-white' />
                )}
              </div>

              {/* Message Bubble */}
              <div
                className={`flex-1 max-w-[80%] ${
                  isUser ? 'text-right' : 'text-left'
                }`}
              >
                <div
                  className={`inline-block p-3 sm:p-4 rounded-2xl shadow-sm message-bubble text-sm sm:text-base ${
                    isUser
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                      : 'bg-white border border-gray-200 text-gray-900'
                  }`}
                >
                  {/* Message Content */}
                  <div
                    className={
                      isUser
                        ? styles.markdownContentUser
                        : styles.markdownContent
                    }
                  >
                    {msg.type === 'raw_text' ? (
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {msg.data}
                      </ReactMarkdown>
                    ) : msg.type === 'user_message' ? (
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {msg.data}
                      </ReactMarkdown>
                    ) : (
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {msg.response?.response?.response ||
                          JSON.stringify(msg, null, 2)}
                      </ReactMarkdown>
                    )}
                  </div>

                  {/* File Attachments */}
                  {msg.files && msg.files.length > 0 && (
                    <div className='mt-2 pt-2 border-t border-gray-200'>
                      <div className='flex flex-wrap gap-2'>
                        {msg.files.map((file, fileIndex: number) => (
                          <div
                            key={fileIndex}
                            className={`inline-flex items-center px-2 py-1 sm:px-3 sm:py-2 rounded-lg text-xs sm:text-sm ${
                              isUser
                                ? 'bg-white/20 text-white'
                                : 'bg-gray-100 text-gray-700'
                            }`}
                          >
                            {getFileIcon(file.name || file.original_name || '')}
                            <span className='ml-2 truncate max-w-[120px] sm:max-w-[150px]'>
                              {file.name || file.original_name}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Timestamp */}
                <div
                  className={`text-xs text-gray-400 mt-1 sm:mt-2 ${
                    isUser ? 'text-right' : 'text-left'
                  }`}
                >
                  {new Date().toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </div>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
};
