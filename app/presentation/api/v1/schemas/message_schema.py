from pydantic import BaseModel
from app.domain.user import User

from datetime import datetime


class MessageBase(BaseModel):
    text: str
    spender: str | User

class MessageCreate(MessageBase):
    created_at: datetime