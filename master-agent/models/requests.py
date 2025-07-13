from typing import Any

from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    session_id: str = Field(..., description="Session ID")
    request_id: str = Field(..., description="Request ID")
    message: str = Field(..., description="Input message from user")
    agents: list[dict[str, Any]] = Field(..., description="List of agents available for user")
