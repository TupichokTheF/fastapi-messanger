from app.domain import BaseEntity
from app.domain.user import User
from app.domain.message.value_objects import MessageText

from dataclasses import dataclass
from datetime import datetime

@dataclass(kw_only=True, eq=False)
class Message(BaseEntity):
    spender: User
    text: MessageText
    created_at: datetime = datetime.now()


@dataclass(kw_only=True, eq=True)
class MessageReceiver:
    message: Message
    receiver: User
    read_at: datetime | None = None

    def mark_as_read(self):
        self.read_at = datetime.now()
        return True
