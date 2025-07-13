from typing import Optional
from pydantic import BaseModel


class FileBase(BaseModel):
    id: str
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    original_name: str


class FileGet(FileBase):
    mimetype: str
    internal_id: str
    internal_name: str
    from_agent: bool


class FileCreate(FileGet):
    pass


class FileUpdate(FileGet):
    pass
