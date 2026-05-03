from app.domain import BaseEntity
from app.domain.user import User
from app.domain.chat import Chat
from app.domain.message.value_objects import MessageText

from dataclasses import dataclass
from datetime import datetime

@dataclass(kw_only=True, eq=False)
class Message(BaseEntity):
    _spender: User
    _chat: Chat
    _text: MessageText
    _created_at: datetime = datetime.now()

    @property
    def text(self):
        return self._text.value

    @property
    def spender(self):
        return self._spender

    @property
    def chat(self):
        return self._chat

    @property
    def created_at(self):
        return self._created_at

    @staticmethod
    def create(spender: User, text: str):
        text = MessageText(text)
        return Message(_spender= spender, _text=text)

