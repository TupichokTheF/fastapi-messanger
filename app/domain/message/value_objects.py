from app.domain import BaseValueObject
from app.domain.message.exceptions import EmptyMessage

from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True, eq=False)
class MessageText(BaseValueObject):
    value: str

    def __post_init__(self):
        raw_value = self.value.strip()
        if not raw_value:
            raise EmptyMessage("The message should consist of at least one character")
