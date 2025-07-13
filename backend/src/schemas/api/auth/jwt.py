from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel


class UserData(BaseModel):
    user_id: Union[UUID, str]


class TokenPayload(BaseModel):
    exp: Optional[int] = None
    sub: Optional[str] = None


class TokenDTO(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None  # TODO: not implemented yet
    token_type: str
