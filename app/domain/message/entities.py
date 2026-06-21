from app.domain import BaseEntity
from app.domain.user import User
from app.domain.chat import Chat
from app.domain.message.value_objects import MessageText

from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(kw_only=True, eq=False)
class Message(BaseEntity):
    _sender: User
    _chat: Chat
    _text: MessageText
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def text(self):
        return self._text.value

    @property
    def sender(self):
        return self._sender

    @property
    def chat(self):
        return self._chat

    @property
    def created_at(self):
        return self._created_at

    @staticmethod
    def create(sender: User, text: str, chat: Chat):
        text = MessageText(text)
        return Message(_sender= sender, _text=text, _chat=chat)

