from pydantic import BaseModel
from app.domain.user import User


class MessageBase(BaseModel):
    text: str
    spender: str | User