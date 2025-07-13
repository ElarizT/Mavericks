import { useState, useCallback, useEffect } from 'react';
import { apiService } from '../services/apiService';
import { LogEntry } from '../types/log';

export const useLogs = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchLogs = useCallback(async (requestId: string) => {
    if (!requestId) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiService.get<LogEntry[]>(`/api/logs/list?request_id=${requestId}`);
      setLogs(response.data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch logs'));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearLogs = useCallback(() => {
    setLogs([]);
    setError(null);
  }, []);

  // Cleanup function
  useEffect(() => {
    return () => {
      setIsLoading(false);
      setError(null);
      setLogs([]);
    };
  }, []);

  return {
    logs,
    isLoading,
    error,
    fetchLogs,
    clearLogs,
  };
}; 