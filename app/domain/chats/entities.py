from app.domain.base.entity import BaseEntity
from app.domain.user.entities import User

from dataclasses import dataclass

@dataclass(kw_only=True, eq=False)
class GroupChat(BaseEntity):
    members: set[User] = None
