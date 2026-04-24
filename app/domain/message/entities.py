from app.domain import BaseEntity
from app.domain.user import User
from app.domain.message.value_objects import MessageText

from dataclasses import dataclass
from datetime import datetime

@dataclass(kw_only=True, eq=False)
class Message(BaseEntity):
    _spender: User
    _text: MessageText
    _created_at: datetime = datetime.now()

    @property
    def text(self):
        return self._text.value

    @property
    def spender(self):
        return self._spender

    @property
    def created_at(self):
        return self._created_at

    @staticmethod
    def create(spender: User, text: str):
        text = MessageText(text)
        return Message(_spender= spender, _text=text)


@dataclass(kw_only=True, eq=True)
class MessageReceiver:
    _message: Message
    _receiver: User
    _read_at: datetime | None = None

    def mark_as_read(self):
        self._read_at = datetime.now()
        return True

    @property
    def receiver(self):
        return self._receiver

    @property
    def message(self):
        return self._message

    @staticmethod
    def create(message: Message, receiver: User):
        return MessageReceiver(_message=message, _receiver=receiver)
