from app.domain.base.entity import BaseEntity
from app.domain.user.entities import User
from app.domain.chat.value_objects import ChatName, ChatType

from dataclasses import dataclass

from datetime import datetime


@dataclass(kw_only=True, eq=False)
class Chat(BaseEntity):
    name: ChatName
    type: ChatType
    members: set[User]
    created_at: datetime = datetime.now()