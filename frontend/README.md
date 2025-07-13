# GenAi Frontend

A React-based frontend application built with Vite, TypeScript, and Material-UI.

## Tech Stack

- React 18
- TypeScript
- Vite
- Material-UI (MUI)
- TailwindCSS
- React Router
- React Flow

## Prerequisites

- [Node.js](https://nodejs.org/en/download/) (LTS version recommended)
- npm (comes with Node.js)

## Environment Variables

The following environment variables are required for the application:

- `VITE_API_URL`: The base URL for the API endpoints
- `VITE_WS_URL`: WebSocket URL for real-time features

Create a `.env` file in the root directory with these variables:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```
More details check here - [Vite Env Variables and Modes](https://vite.dev/guide/env-and-mode)

## Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## Production

### Building

To build the application for production:

```bash
npm run build
```

The build output will be in the `dist` directory.

### Running in Production

1. Using npm:
   ```bash
   npm run prod
   ```
   The application will be available at `http://localhost:3000`

2. Using Docker:
   ```bash
   # Build the Docker image
   docker build -t genai-frontend .
   
   # Run the container
   docker run -p 3000:3000 genai-frontend
   ```
   The application will be available at `http://localhost:3000`

   Note: The `-p 3000:3000` flag maps the container's port 3000 to your host machine's port 3000. 
   You can change the host port by modifying the first number (e.g., `-p 8080:3000` to access via `http://localhost:8080`).

## Testing

Run the test suite:

```bash
npm test
```

## Port Configuration

The application uses different ports in various environments. Here's how to change them:

### Development Server (Vite)
The development server port is configured in `vite.config.ts`:
```typescript
server: {
  port: 3000,
  open: true,
}
```
For more details, see [Vite Server Options](https://vitejs.dev/config/server-options.html)

### Production Server (serve)
The production server port is configured in two places:

1. In `Dockerfile`:
```dockerfile
EXPOSE 3000
CMD [ "serve", "-s", "dist", "-l", "3000" ]
```

2. When running with Docker, you can map to a different host port:
```bash
# Map container port 3000 to host port 8080
docker run -p 8080:3000 genai-frontend
```

For more details about serve configuration, see [serve-handler options](https://github.com/vercel/serve-handler#options)

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run preview`: Preview production build
- `npm run prod`: Build and preview production build
- `npm run lint`: Run ESLint
- `npm test`: Run Jest tests

## Project Structure

- `src/`: Source code directory
  - `components/`: Reusable React components
  - `pages/`: Page components
  - `services/`: API and service functions
  - `types/`: TypeScript type definitions
  - `utils/`: Utility functions
  - `App.tsx`: Main application component
  - `main.tsx`: Application entry point
