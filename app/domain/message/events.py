from app.domain.base import BaseEvent

from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True)
class MessageReceivedEvent(BaseEvent):
    message_id: int
    chat_id: int
    sender_id: int
    text: str
    created_at: datetime