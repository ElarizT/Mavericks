import Link from 'next/link';
import {
  MessageCircle,
  Bot,
  Sparkles,
  Shield,
  Zap,
  ArrowRight,
  User,
} from 'lucide-react';
import TeamSection from '@/components/TeamSection';
import TopBanner from '@/components/TopBanner';
import DemoSection from '@/components/DemoSection';

export default function Home() {
  return (
    <div className='min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex flex-col'>
      <TopBanner />
      {/* Header */}
      <header className='sticky top-0 z-30 bg-white/80 backdrop-blur border-b border-gray-200 shadow-sm'>
        <nav className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex justify-between items-center py-3'>
            <div className='flex items-center space-x-2'>
              <div className='w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center'>
                <Bot className='w-5 h-5 text-white' />
              </div>
              <span className='text-xl font-bold text-gray-900'>LawCo AI</span>
            </div>
            <div className='hidden md:flex items-center space-x-8'>
              <a
                href='#features'
                className='text-gray-600 hover:text-blue-700 transition-colors'
              >
                Features
              </a>
              <a
                href='#how'
                className='text-gray-600 hover:text-blue-700 transition-colors'
              >
                How it Works
              </a>
              <a
                href='#team'
                className='text-gray-600 hover:text-blue-700 transition-colors'
              >
                Team
              </a>
              <a
                href='#action'
                className='text-gray-600 hover:text-blue-700 transition-colors'
              >
                Action
              </a>
              <a
                href='https://github.com/your-org/your-repo'
                target='_blank'
                rel='noopener noreferrer'
                className='flex items-center gap-2 border border-gray-300 px-4 py-2 rounded-full text-gray-700 hover:bg-gray-100 transition-colors font-medium text-sm ml-2'
                aria-label='GitHub Repository'
              >
                <span>⚡</span>
                GitHub
              </a>
              <Link
                href='/chat'
                className='bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-full hover:from-blue-700 hover:to-purple-700 transition-all duration-200 flex items-center space-x-2'
              >
                <span>Try Chat</span>
                <ArrowRight className='w-4 h-4' />
              </Link>
            </div>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className='flex-1'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 pb-8'>
          <div className='text-center'>
            <div className='inline-flex items-center px-4 py-1.5 rounded-full bg-blue-100 text-blue-800 text-sm font-medium mb-6'>
              <Sparkles className='w-4 h-4 mr-2' /> Powered by Advanced AI
            </div>
            <h1 className='text-4xl md:text-6xl font-bold text-gray-900 mb-4 leading-tight'>
              Your Intelligent{' '}
              <span className='gradient-text'>Legal Assistant</span>
            </h1>
            <p className='text-lg text-gray-600 mb-6 max-w-2xl mx-auto leading-relaxed'>
              Get instant legal insights, document analysis, and professional
              guidance through our advanced AI-powered chatbot. Upload
              documents, ask questions, and receive comprehensive legal
              assistance.
            </p>
            <div className='flex flex-col sm:flex-row gap-3 justify-center items-center mb-8'>
              <Link
                href='/chat'
                className='bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-full hover:from-blue-700 hover:to-purple-700 transition-all duration-200 flex items-center space-x-2 text-lg font-semibold shadow-lg hover:shadow-xl hover-lift'
              >
                <MessageCircle className='w-5 h-5' />
                <span>Start Chatting</span>
              </Link>
              <button className='border-2 border-gray-300 text-gray-700 px-8 py-3 rounded-full hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 text-lg font-semibold'>
                Watch Demo
              </button>
            </div>
          </div>
        </div>
        {/* How it Works Section */}
        <section id='how' className='py-10 bg-white border-y border-gray-100'>
          <div className='max-w-6xl mx-auto px-4 sm:px-6 lg:px-8'>
            <div className='text-center mb-10'>
              <h2 className='text-2xl md:text-3xl font-bold text-gray-900 mb-2'>
                How It Works
              </h2>
              <p className='text-base text-gray-600 max-w-xl mx-auto'>
                Using LawCo AI is simple and secure. Here’s how you can get
                started in just a few steps.
              </p>
            </div>
            <div className='grid md:grid-cols-3 gap-6'>
              <div className='flex flex-col items-center text-center p-6 rounded-xl bg-blue-50 border border-blue-100'>
                <div className='w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mb-3'>
                  <User className='w-6 h-6 text-white' />
                </div>
                <h3 className='font-semibold text-lg mb-1'>
                  1. Ask a Question
                </h3>
                <p className='text-gray-600 text-sm'>
                  Type your legal question or upload a document to get started.
                </p>
              </div>
              <div className='flex flex-col items-center text-center p-6 rounded-xl bg-green-50 border border-green-100'>
                <div className='w-12 h-12 bg-gradient-to-r from-green-600 to-emerald-600 rounded-full flex items-center justify-center mb-3'>
                  <Shield className='w-6 h-6 text-white' />
                </div>
                <h3 className='font-semibold text-lg mb-1'>2. AI Analyzes</h3>
                <p className='text-gray-600 text-sm'>
                  Our AI reviews your input and provides instant, reliable legal
                  insights.
                </p>
              </div>
              <div className='flex flex-col items-center text-center p-6 rounded-xl bg-purple-50 border border-purple-100'>
                <div className='w-12 h-12 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center mb-3'>
                  <Zap className='w-6 h-6 text-white' />
                </div>
                <h3 className='font-semibold text-lg mb-1'>3. Get Results</h3>
                <p className='text-gray-600 text-sm'>
                  Receive clear answers, document summaries, and actionable
                  advice.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id='features' className='py-8 sm:py-12 bg-white'>
          <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
            <div className='mb-8 sm:mb-12 text-left sm:text-center'>
              <h2 className='text-2xl sm:text-3xl font-bold text-gray-900 mb-2'>
                Powerful Features
              </h2>
              <p className='text-base sm:text-lg text-gray-600 max-w-2xl mx-auto'>
                Everything you need for comprehensive legal assistance
              </p>
            </div>
            <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8'>
              <div className='bg-white border border-gray-100 rounded-2xl p-5 sm:p-6 flex items-start gap-4 transition-shadow hover:shadow-lg focus-within:shadow-lg cursor-pointer'>
                <div className='flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center bg-blue-100'>
                  <MessageCircle className='w-7 h-7 text-blue-600' />
                </div>
                <div>
                  <h3 className='text-base sm:text-lg font-bold text-black mb-1 sm:mb-2'>
                    Smart Conversations
                  </h3>
                  <p className='text-gray-600 text-sm sm:text-base'>
                    Engage in natural conversations with our AI that understands
                    legal context and terminology.
                  </p>
                </div>
              </div>
              <div className='bg-white border border-gray-100 rounded-2xl p-5 sm:p-6 flex items-start gap-4 transition-shadow hover:shadow-lg focus-within:shadow-lg cursor-pointer'>
                <div className='flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center bg-green-100'>
                  <Shield className='w-7 h-7 text-green-600' />
                </div>
                <div>
                  <h3 className='text-base sm:text-lg font-bold text-black mb-1 sm:mb-2'>
                    Document Analysis
                  </h3>
                  <p className='text-gray-600 text-sm sm:text-base'>
                    Upload legal documents and get instant analysis, summaries,
                    and key insights.
                  </p>
                </div>
              </div>
              <div className='bg-white border border-gray-100 rounded-2xl p-5 sm:p-6 flex items-start gap-4 transition-shadow hover:shadow-lg focus-within:shadow-lg cursor-pointer'>
                <div className='flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center bg-purple-100'>
                  <Zap className='w-7 h-7 text-purple-600' />
                </div>
                <div>
                  <h3 className='text-base sm:text-lg font-bold text-black mb-1 sm:mb-2'>
                    Instant Responses
                  </h3>
                  <p className='text-gray-600 text-sm sm:text-base'>
                    Get immediate answers to your legal questions with our
                    lightning-fast AI system.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <DemoSection />

        <section id='team'>
          <TeamSection />
        </section>

        <section
          id='action'
          className='py-16 bg-white border-t border-gray-100'
        >
          <div className='max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center'>
            <h2 className='text-3xl md:text-4xl font-bold text-gray-900 mb-4'>
              Action Section
            </h2>
            <p className='text-xl text-gray-600 mb-8'>
              This is a placeholder for another important section.
            </p>
          </div>
        </section>
      </main>
      {/* Footer */}
      <footer className='bg-gray-950 text-gray-200 border-t border-gray-800 pt-12 pb-6 mt-8'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex flex-col md:flex-row justify-between gap-10'>
            {/* Left: Logo and description */}
            <div className='mb-8 md:mb-0 md:w-1/3 flex flex-col items-start'>
              <div className='flex items-center space-x-2 mb-3'>
                <div className='w-9 h-9 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center'>
                  <Bot className='w-6 h-6 text-white' />
                </div>
                <span className='text-2xl font-bold text-white'>LawCo AI</span>
              </div>
              <p className='text-gray-400 text-sm max-w-xs'>
                Your intelligent legal assistant for instant insights, document
                analysis, and professional guidance.
              </p>
            </div>
            {/* Right: Navigation links */}
            <div className='flex-1 grid grid-cols-2 sm:grid-cols-3 gap-8'>
              <div>
                <h4 className='text-gray-100 font-semibold mb-3 text-sm uppercase tracking-wider'>
                  Product
                </h4>
                <ul className='space-y-2'>
                  <li>
                    <a
                      href='#features'
                      className='hover:text-white text-gray-400 text-sm'
                    >
                      Features
                    </a>
                  </li>
                  <li>
                    <a
                      href='#how'
                      className='hover:text-white text-gray-400 text-sm'
                    >
                      How it Works
                    </a>
                  </li>
                  <li>
                    <a
                      href='/chat'
                      className='hover:text-white text-gray-400 text-sm'
                    >
                      Try Chat
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className='text-gray-100 font-semibold mb-3 text-sm uppercase tracking-wider'>
                  Company
                </h4>
                <ul className='space-y-2'>
                  <li>
                    <a
                      href='#'
                      className='hover:text-white text-gray-400 text-sm'
                    >
                      About
                    </a>
                  </li>
                  <li>
                    <a
                      href='#'
                      className='hover:text-white text-gray-400 text-sm'
                    >
                      Contact
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className='text-gray-100 font-semibold mb-3 text-sm uppercase tracking-wider'>
                  Legal
                </h4>
                <ul className='space-y-2'>
                  <li>
                    <a
                      href='#'
                      className='hover:text-white text-gray-400 text-sm'
                    >
                      Privacy Policy
                    </a>
                  </li>
                  <li>
                    <a
                      href='#'
                      className='hover:text-white text-gray-400 text-sm'
                    >
                      Terms of Service
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div className='border-t border-gray-800 mt-10 pt-6 text-center text-xs text-gray-500'>
            © 2024 LawCo AI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
