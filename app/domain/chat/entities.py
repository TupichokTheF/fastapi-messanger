from app.domain.base.entity import BaseEntity
from app.domain.user.entities import User
from app.domain.chat.value_objects import ChatName, ChatType
from app.domain.chat.exceptions import UserAlreadyAdded

from dataclasses import dataclass, field

from datetime import datetime, timezone


@dataclass(kw_only=True, eq=False)
class ChatMember:
    _chat: "Chat"
    _member: User
    _created_at: datetime = datetime.now()

    @staticmethod
    def create(member_: User, chat_: "Chat"):
        return ChatMember(_member=member_, _chat=chat_)


@dataclass(kw_only=True, eq=False)
class Chat(BaseEntity):
    _name: ChatName
    _type: ChatType
    _members: set[ChatMember] = field(default_factory=set)
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def add_members(self, members: set[User]):
        if self._members & members:
            raise UserAlreadyAdded("User already member")
        for member in members:
            chat_member = ChatMember.create(member, self)
            self._members.add(chat_member)


    @staticmethod
    def create(name_: str, members_: set[User], type_: ChatType):
        name_ = ChatName(name_)
        chat = Chat(_name=name_, _type=type_)
        chat.add_members(members_)
        return chat




