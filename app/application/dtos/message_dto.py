from dataclasses import dataclass
from datetime import datetime

from app.domain.message import Message


@dataclass(kw_only=True)
class MessageDTO:
    id: int
    sender: str
    created_at: datetime
    text: str

    @classmethod
    def from_entity(cls, message_: Message):
        return cls(id=message_.id,
                   sender=message_.sender,
                   created_at=message_.created_at,
                   text=message_.text)