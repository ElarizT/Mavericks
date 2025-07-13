from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class RegisterResponse(BaseModel):
    id: str
    username: str


class AgentSchema(BaseModel):
    agent_id: str
    agent_name: str
    agent_description: str
    agent_input_schema: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    agent_jwt: Optional[str] = None
