from app.domain.message import Message

from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass(kw_only=True)
class MessageDTO:
    message_id: int
    sender_id: int
    chat_id: int
    text: str
    created_at: datetime

    def as_dict(self):
        return asdict(self)

    @classmethod
    def from_entity(cls, message_: Message):
        return cls(message_id=message_.id,
                   sender_id=message_.sender.id,
                   chat_id=message_.chat.id,
                   text=message_.text,
                   created_at=message_.created_at)
