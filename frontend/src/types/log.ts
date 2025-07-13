export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARNING = 'warning',
  ERROR = 'error',
  CRITICAL = 'critical'
}

export interface LogEntry {
  id: string;
  session_id: string;
  request_id: string;
  log_level: LogLevel;
  message: string;
  creator_id: string | null;
  agent_id: string;
  created_at: string;
  updated_at: string;
}

export type Log = LogEntry; 