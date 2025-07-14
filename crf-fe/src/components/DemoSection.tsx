import { Bot, FileText, Send } from "lucide-react";

export default function DemoSection() {
  return (
    <section className="py-16 bg-transparent">
      <div className="max-w-6xl mx-auto px-2 sm:px-4">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-10 text-center">
          See LawCo AI in Action
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-10">
          {/* AI Chat Demo */}
          <div className="bg-white/90 rounded-3xl shadow-lg p-4 sm:p-8 flex flex-col min-h-[340px] transition-shadow hover:shadow-2xl border border-blue-100">
            <div className="flex items-center gap-2 mb-4">
              <Bot className="w-7 h-7 text-blue-500" />
              <h3 className="text-xl sm:text-2xl font-bold text-gray-900">
                LawCo AI Assistant
              </h3>
            </div>
            <div className="flex flex-col gap-3 flex-1">
              <div className="self-start bg-blue-100/70 text-gray-800 rounded-xl px-4 py-3 max-w-[90%] text-base sm:text-lg">
                Hello! How can I assist you with your legal needs today?
              </div>
              <div className="self-end bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl px-4 py-3 max-w-[90%] text-base sm:text-lg shadow-md">
                Can you review this contract for key risks?
              </div>
            </div>
            <div className="mt-6 flex items-center gap-2">
              <input
                type="text"
                className="flex-1 border border-gray-200 rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-200 bg-white/80 text-base"
                placeholder="Type your message..."
                disabled
              />
              <button
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-xl p-2 transition-colors duration-200"
                disabled
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Generated Content Demo */}
          <div className="bg-white/90 rounded-3xl shadow-lg p-4 sm:p-8 flex flex-col min-h-[340px] transition-shadow hover:shadow-2xl border border-blue-100">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-7 h-7 text-blue-500" />
              <h3 className="text-xl sm:text-2xl font-bold text-gray-900">
                AI-Powered Analysis
              </h3>
            </div>
            <div className="flex-1 flex flex-col justify-center">
              <div className="bg-blue-100/70 rounded-xl p-4 sm:p-6 min-h-[120px]">
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-3 h-3 bg-red-400 rounded-full inline-block"></span>
                  <span className="w-3 h-3 bg-yellow-300 rounded-full inline-block"></span>
                  <span className="w-3 h-3 bg-green-400 rounded-full inline-block"></span>
                </div>
                <div className="text-gray-800 text-base sm:text-lg">
                  <strong>Summary:</strong> This contract contains a non-compete
                  clause, confidentiality obligations, and a 30-day termination
                  notice. <br />
                  <strong>Risks:</strong> The non-compete duration is 3 years,
                  which may be unenforceable in some jurisdictions. <br />
                  <strong>Recommendation:</strong> Consider reducing the
                  non-compete period and clarifying the scope of confidential
                  information.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
