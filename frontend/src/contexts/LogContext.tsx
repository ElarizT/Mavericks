import type { FC, ReactNode } from 'react';
import { createContext, useContext, useState, useCallback } from 'react';

export interface LogEntry {
  id: string;
  session_id: string;
  request_id: string;
  log_level: string;
  message: string;
  creator_id: string | null;
  agent_id: string;
  created_at: string;
  updated_at: string;
}

interface LogContextType {
  logs: LogEntry[];
  addLog: (log: Omit<LogEntry, 'id' | 'created_at' | 'updated_at'>) => void;
}

const LogContext = createContext<LogContextType | undefined>(undefined);

export const useLogs = () => {
  const context = useContext(LogContext);
  if (!context) {
    throw new Error('useLogs must be used within a LogProvider');
  }
  return context;
};

interface LogProviderProps {
  children: ReactNode;
}

export const LogProvider: FC<LogProviderProps> = ({ children }) => {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  const addLog = useCallback((log: Omit<LogEntry, 'id' | 'created_at' | 'updated_at'>) => {
    const newLog: LogEntry = {
      ...log,
      id: Date.now().toString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    setLogs(prevLogs => [...prevLogs, newLog]);
  }, []);

  return (
    <LogContext.Provider value={{ logs, addLog }}>
      {children}
    </LogContext.Provider>
  );
}; 