import { Bot } from "lucide-react";

export const TypingIndicator = () => {
  return (
    <div className="absolute bottom-4 left-4 flex items-start space-x-3">
      {/* Avatar */}
      <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center bg-gradient-to-r from-gray-600 to-gray-700">
        <Bot className="w-5 h-5 text-white" />
      </div>

      {/* Typing Bubble */}
      <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
        <div className="flex items-center space-x-1">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
          </div>
          <span className="text-sm text-gray-500 ml-2">AI is thinking...</span>
        </div>
      </div>
    </div>
  );
};
