from pydantic import BaseModel


class Message(BaseModel):
    client_id: str
    message: dict


class MessageResponse(BaseModel):
    detail: str
