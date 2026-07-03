from dataclasses import dataclass
from datetime import datetime

from app.domain.chat import Chat, ChatMember, ChatType


@dataclass(kw_only=True)
class ChatDTO:
    id: int
    name: str
    type: ChatType
    created_at: datetime
    members: set[ChatMember]

    @classmethod
    def from_entity(cls, chat: Chat) -> "ChatDTO":
        return cls(id=chat.id,
                   name=chat.name,
                   type=chat.type,
                   created_at=chat.created_at,
                   members=chat.members)
