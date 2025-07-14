# LawCo AI – Frontend

LawCo AI is an intelligent legal assistant web app that helps users analyze legal documents, ask legal questions, and get instant AI-powered insights. This frontend connects to an AgentOS backend to provide real-time AI conversations and document analysis.

---

## 🚀 Features

- **AI-Powered Legal Chat:** Instantly ask legal questions and get expert-level answers from the AI assistant
- **Document Upload & Analysis:** Upload contracts or legal documents and receive detailed summaries, risk analysis, and recommendations
- **Real-Time WebSocket Chat:** Enjoy seamless, real-time conversations with the AI for a smooth user experience
- **Markdown Support:** Rich text formatting for code blocks, lists, and other markdown elements in chat
- **File Management:** Upload multiple files with visual feedback and retry functionality
- **Modern, Responsive UI:** Fully responsive design with beautiful gradients, animations, and accessibility in mind

---

## 🛠️ Tech Stack

- **Framework:** [Next.js 15](https://nextjs.org/) (React 19)
- **Styling:** [Tailwind CSS 4](https://tailwindcss.com/)
- **Icons:** [Lucide React](https://lucide.dev/)
- **Markdown:** [react-markdown](https://github.com/remarkjs/react-markdown) with GitHub Flavored Markdown
- **Language:** TypeScript
- **Backend Integration:** AgentOS REST API + WebSocket

---

## 📋 Prerequisites

Before setting up the frontend, ensure you have:

1. **Node.js** (v18 or higher)
2. **npm** or **yarn** package manager
3. **AgentOS Backend** running (see Backend Setup section)
4. **AgentOS Account** credentials

Make sure your AgentOS backend is running via Docker:
---

## 🔧 Frontend Setup

### 1. **Clone the Repository**

```bash
git clone https://github.com/your-org/crf-fe.git
cd crf-fe
```

### 2. **Install Dependencies**

```bash
npm install
```

### 3. **Environment Configuration**

Create a `.env.local` file in the project root:

```bash
# AgentOS Account Credentials
# Replace with your actual AgentOS account credentials
NEXT_PUBLIC_AUTH_USERNAME=your_agentos_username
NEXT_PUBLIC_AUTH_PASSWORD=your_agentos_password
```

**⚠️ Important:** 
- Replace `your_agentos_username` and `your_agentos_password` with the actual credentials you used to create your AgentOS account
- These credentials are used for automatic authentication in `ChatContainer.tsx` (line 56)

### 4. **Update Authentication (Alternative Method)**

If you prefer not to use environment variables, you can directly update the credentials in the code:

```typescript
// src/components/chat/ChatContainer.tsx (around line 56)
user = await authService.login("your_username", "your_password");
```

### 5. **Run the Development Server**

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📦 Dependencies

### Core Dependencies
```json
{
  "next": "15.3.5",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "typescript": "^5"
}
```

### UI & Styling
```json
{
  "tailwindcss": "^4",
  "lucide-react": "^0.525.0",
  "class-variance-authority": "^0.7.1",
  "clsx": "^2.1.1",
  "tailwind-merge": "^3.3.1"
}
```

### Markdown & Rich Text
```json
{
  "react-markdown": "^9.0.0",
  "remark-gfm": "^4.0.0"
}
```

### File Handling
```json
{
  "react-dropzone": "^14.3.8",
  "uuid": "^11.1.0",
  "@types/uuid": "^10.0.0"
}
```

### Development Dependencies
```json
{
  "eslint": "^9",
  "eslint-config-next": "15.3.5",
  "@types/node": "^20",
  "@types/react": "^19",
  "@types/react-dom": "^19"
}
```

---

## 🗂️ Project Structure

```
crf-fe/
├── src/
│   ├── app/                    # Next.js app directory
│   │   ├── api/               # API routes
│   │   ├── chat/              # Chat page
│   │   └── layout.tsx         # Root layout
│   ├── components/            # React components
│   │   ├── chat/              # Chat-related components
│   │   │   ├── ChatContainer.tsx
│   │   │   ├── ChatDisplay.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── TypingIndicator.tsx
│   │   ├── document/          # Document components
│   │   ├── file-upload/       # File upload components
│   │   ├── layout/            # Layout components
│   │   ├── providers/         # Context providers
│   │   └── ui/                # UI components
│   ├── contexts/              # React contexts
│   ├── hooks/                 # Custom hooks
│   ├── lib/                   # Utility functions
│   ├── services/              # API services
│   │   ├── apiService.ts      # REST API client
│   │   ├── authService.ts     # Authentication
│   │   ├── chatService.ts     # Chat functionality
│   │   ├── fileUploadService.ts # File handling
│   │   └── websocketService.ts # WebSocket client
│   └── types/                 # TypeScript types
├── public/                    # Static assets
├── .env.local                 # Environment variables (create this)
├── package.json
└── README.md
```

---

## 🔌 API Integration

### REST API Endpoints

The frontend connects to these AgentOS backend endpoints:

- **Authentication:** `POST /api/login/access-token`
- **Models:** `GET /api/models`
- **File Upload:** `POST /files`
- **File Download:** `GET /files/{id}`

### WebSocket Connection

- **URL:** `ws://localhost:8000/frontend/ws`
- **Authentication:** Token-based via query parameter
- **Message Format:** JSON with support for user messages and agent responses

---

## 💬 Usage

### 1. **Starting a Chat**
- The app automatically authenticates using your AgentOS credentials
- Type messages in the chat input at the bottom
- The AI will respond in real-time via WebSocket

### 2. **Uploading Files**
- Click the paperclip icon to attach files
- Supported formats: PDF, images, text files, Word documents
- Files are uploaded immediately and show progress indicators
- Remove files using the X button or retry failed uploads

### 3. **Markdown Support**
Chat messages support full markdown formatting:
- **Bold** and *italic* text
- `code blocks` and inline code
- Lists (ordered and unordered)
- Headers and blockquotes
- Tables

---

## 🛠️ Development

### Available Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Linting
npm run lint
```

### Building for Production

```bash
npm run build
npm start
```

---

## 🔧 Configuration

### File Upload Limits

Current file upload limits (configurable in `fileUploadService.ts`):
- **Max file size:** 50MB
- **Supported types:** Images, PDF, text, Word docs, Excel files

---

## 🐛 Troubleshooting

### Common Issues

1. **"WebSocket connection failed"**
   - Ensure AgentOS backend is running on port 8000
   - Check that WebSocket endpoint `/frontend/ws` is accessible

2. **"Authentication failed"**
   - Verify your AgentOS username and password in `.env.local`
   - Check that credentials match your AgentOS account

3. **"File upload failed"**
   - Ensure file size is under 50MB
   - Check that file type is supported
   - Verify backend file upload endpoint is working

4. **Backend connection issues**
   - Confirm Docker container is running: `docker ps`
   - Test API endpoint: `curl http://localhost:8000/health`
   - Check Docker logs: `docker logs agentos-backend`

### Debugging

Enable debug logs by checking the browser console. The app logs:
- Authentication status
- WebSocket connection events
- File upload progress
- API responses

---

## 🤝 Contributing

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📬 Support

For questions, issues, or support:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review AgentOS documentation for backend setup

---

> **Note:** This frontend is designed to work specifically with AgentOS backend. Ensure your AgentOS instance is properly configured and running before starting the frontend application.
