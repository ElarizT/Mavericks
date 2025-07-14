'use client';

import { ChatContainer } from '@/components/chat';
import {
  Bot,
  Plus,
  MessageSquare,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { useState } from 'react';
// Mock data for right sidebar
const mockKeyTerminology = [
  {
    title:
      'This section will have a summarized version of the highlighted key terminology and legal jargon',
    context: 'Click to view in context',
  },
  {
    title:
      'Each section will have a summarized version of the highlighted key terminology and legal jargon',
    context: 'Click to view in context',
  },
  {
    title:
      'Clicking on the highlighted key terminology will open a new section with the full context of the term within the conversation',
    context: 'Click to view in context',
  },
];

const mockChats = [
  { id: '1', title: 'Document Analysis Introduction' },
  { id: '2', title: 'GitHub Repository Documentation' },
];

export default function ChatPage() {
  const [selectedChat, setSelectedChat] = useState('1');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true);

  return (
    <div className='min-h-screen flex bg-white'>
      {/* Sidebar */}
      <aside
        className={`transition-all duration-300 h-screen sticky top-0 z-40 flex flex-col ${
          sidebarOpen ? 'w-72' : 'w-0'
        } bg-white border-r border-gray-200`}
        style={{ minWidth: sidebarOpen ? '18rem' : '0', overflow: 'hidden' }}
      >
        {/* Sidebar content */}
        <div className={sidebarOpen ? 'flex flex-col h-full' : 'hidden'}>
          {/* Branding */}
          <div className='flex items-center gap-2 px-4 py-4 border-b border-gray-100'>
            <div className='w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center'>
              <Bot className='w-5 h-5 text-white' />
            </div>
            <div>
              <h1 className='text-base font-bold text-gray-900 leading-tight'>
                LawCo AI Assistant
              </h1>
              <p className='text-xs text-gray-500'>
                Your intelligent legal companion
              </p>
            </div>
          </div>
          {/* New Chat Button */}
          <button className='flex items-center gap-2 px-4 py-2 text-blue-600 hover:bg-blue-50 transition-colors font-medium border-b border-gray-100 text-sm'>
            <Plus className='w-4 h-4' />
            New Chat
          </button>
          {/* Chat List */}
          <nav className='flex-1 overflow-y-auto px-1 py-2'>
            {mockChats.map((chat) => (
              <button
                key={chat.id}
                onClick={() => setSelectedChat(chat.id)}
                className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg mb-1 text-left transition-colors font-medium text-gray-700 hover:bg-blue-100/60 hover:text-blue-700 text-sm ${
                  selectedChat === chat.id ? 'bg-blue-100/80 text-blue-700' : ''
                }`}
              >
                <MessageSquare className='w-4 h-4' />
                <span className='truncate'>{chat.title}</span>
              </button>
            ))}
          </nav>
          {/* Footer */}
          <div className='px-4 py-3 border-t border-gray-100 text-xs text-gray-400'>
            © 2024 LawCo AI
          </div>
        </div>
        {/* Sidebar toggle button (collapse) - always visible and centered */}
        <button
          className='fixed left-[17.5rem] top-1/2 z-50 w-8 h-8 bg-white border border-gray-200 rounded-full shadow flex items-center justify-center transition-all duration-200'
          style={{
            transform: 'translateY(-50%)',
            display: sidebarOpen ? 'flex' : 'none',
          }}
          onClick={() => setSidebarOpen(false)}
          aria-label='Collapse sidebar'
        >
          <ChevronLeft className='w-5 h-5 text-gray-500' />
        </button>
      </aside>
      {/* Sidebar open button (when collapsed) - always visible and centered */}
      {!sidebarOpen && (
        <button
          className='fixed left-2 top-1/2 z-50 w-8 h-8 bg-white border border-gray-200 rounded-full shadow flex items-center justify-center transition-all duration-200'
          style={{ transform: 'translateY(-50%)' }}
          onClick={() => setSidebarOpen(true)}
          aria-label='Expand sidebar'
        >
          <ChevronRight className='w-5 h-5 text-gray-500' />
        </button>
      )}

      {/* Main Chat Area + Right Sidebar */}
      <div className='flex-1 flex h-screen transition-all duration-300'>
        {/* Main Chat Area */}
        <main className='flex-1 flex flex-col h-full bg-white'>
          {/* Header - hide when sidebar is hidden for full-screen chat */}
          {sidebarOpen && (
            <header className='bg-white border-b border-gray-200 sticky top-0 z-30'>
              <div className='max-w-6xl mx-auto px-6 flex items-center justify-between h-16'>
                <div className='flex items-center gap-3'>
                  <div className='w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center'>
                    <Bot className='w-5 h-5 text-white' />
                  </div>
                  <span className='font-semibold text-gray-900 text-base'>
                    {mockChats.find((c) => c.id === selectedChat)?.title ||
                      'New Chat'}
                  </span>
                </div>
              </div>
            </header>
          )}
          {/* Chat Container - always full height, no extra margin/padding/border/shadow/rounded */}
          <div className='flex-1 flex flex-col w-full h-full p-0 m-0 bg-white transition-all duration-300'>
            {/* Force enable input for design/dev */}
            <ChatContainer forceEnableInput fullScreen={!sidebarOpen} />
          </div>
        </main>
        {/* Right Sidebar (Key Terminology) */}
        {rightSidebarOpen ? (
          <aside className='hidden lg:flex flex-col w-80 h-full border-l border-gray-200 bg-gray-50 p-4 overflow-y-auto relative'>
            {/* Close button */}
            <button
              className='absolute top-4 right-4 w-10 h-10 flex items-center justify-center rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors'
              onClick={() => setRightSidebarOpen(false)}
              aria-label='Close right sidebar'
            >
              <ChevronLeft className='w-6 h-6 text-gray-300' />
            </button>
            <h2 className='text-lg font-semibold mb-4 mt-2'>Key Terminology</h2>
            <div className='space-y-4 mt-2'>
              {mockKeyTerminology.map((item, idx) => (
                <div
                  key={idx}
                  className='bg-white rounded-lg border border-gray-100 p-4 shadow-sm'
                >
                  <div className='text-sm text-gray-900 mb-2'>{item.title}</div>
                  <button className='text-xs text-blue-600 hover:underline'>
                    {item.context}
                  </button>
                </div>
              ))}
            </div>
          </aside>
        ) : (
          <button
            className='hidden lg:flex fixed right-4 top-24 z-50 w-12 h-12 items-center justify-center rounded-2xl bg-gray-800 hover:bg-gray-700 transition-colors shadow'
            onClick={() => setRightSidebarOpen(true)}
            aria-label='Open right sidebar'
          >
            <ChevronLeft className='w-7 h-7 text-gray-300' />
          </button>
        )}
      </div>
    </div>
  );
}
