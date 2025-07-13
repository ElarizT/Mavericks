from datetime import datetime
from pydantic import BaseModel


class UserDTO(BaseModel):
    username: str
    created_at: datetime
    updated_at: datetime
