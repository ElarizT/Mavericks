from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel


class LogBase(BaseModel):
    session_id: Union[str, UUID]
    request_id: Union[str, UUID]
    log_level: str
    message: str


class LogCreate(LogBase):
    creator_id: Optional[str] = None
    agent_id: str


class LogUpdate(LogBase):
    pass


class LogEntry(LogCreate):
    created_at: datetime
    updated_at: datetime


class LogEntryDTO(LogEntry):
    pass


class FrontendLogEntryDTO(BaseModel):
    type: str  # TODO: enum
    log: LogEntry
