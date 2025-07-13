// Get environment variables with Node.js process.env
const getEnvVar = (key: string, defaultValue: string): string => {
  return (import.meta as unknown as {env: any}).env?.[`VITE_${key}`] || defaultValue;
};

export const environment = {
  apiBaseUrl: getEnvVar('API_URL', 'http://localhost:8000'),
  wsBaseUrl: getEnvVar('WS_URL', 'ws://localhost:8000'),
}; 