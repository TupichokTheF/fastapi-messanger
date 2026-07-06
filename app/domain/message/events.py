from app.domain.base import BaseEvent

from dataclasses import dataclass


@dataclass(kw_only=True)
class MessageSentEvent(BaseEvent):
    message_id: int
    chat_id: int
    sender_id: int
    text: str
    created_at_timestamp_ms: int
