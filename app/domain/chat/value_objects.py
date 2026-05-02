from app.domain.base import BaseValueObject
from app.domain.chat.exceptions import IncorrectNameError

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class ChatName(BaseValueObject):
    value: str | None

    def __post_init__(self):
        if not self.value:
            return
        if not self.value.strip():
            raise IncorrectNameError("Incorrect name of chat")
        if len(self.value) > 40:
            raise IncorrectNameError("Name of the chat is too long")


class ChatType(StrEnum):
    DIRECT = "direct"
    GROUP = "group"