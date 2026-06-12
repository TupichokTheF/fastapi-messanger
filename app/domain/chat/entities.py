from app.domain.base.entity import BaseEntity
from app.domain.user.entities import User
from app.domain.chat.value_objects import ChatName, ChatType
from app.domain.chat.exceptions import UserAlreadyAdded, IncorrectChatMembers

from dataclasses import dataclass, field

from datetime import datetime, timezone


@dataclass(kw_only=True, eq=False)
class ChatMember(BaseEntity):
    _chat: "Chat"
    _member: User
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def user(self):
        return self._member

    @property
    def chat(self):
        return self._chat

    @staticmethod
    def create(member_: User, chat_: "Chat"):
        return ChatMember(_member=member_, _chat=chat_)


@dataclass(kw_only=True, eq=False)
class Chat(BaseEntity):
    _name: ChatName
    _type: ChatType
    _members: set[ChatMember] = field(default_factory=set)
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def created_at(self):
        return self._created_at

    @property
    def name(self):
        return self._name.value

    @property
    def type(self):
        return self._type

    @property
    def members(self):
        return self._members

    def add_members(self, members: set[User]):
        existing_users = {member.user for member in self.members}
        if existing_users & members:
            raise UserAlreadyAdded("User already member")
        for member in members:
            chat_member = ChatMember.create(member, self)
            self._members.add(chat_member)

    @staticmethod
    def create(name_: str, members_: set[User], type_: ChatType):
        if len(members_) < 1:
            raise IncorrectChatMembers("Incorrect count of members for direct chat")
        if type_ == ChatType.DIRECT and len(members_) != 2:
            raise IncorrectChatMembers("Incorrect count of members for direct chat")
        name_ = ChatName(name_)
        chat = Chat(_name=name_, _type=type_)
        chat.add_members(members_)
        return chat


@dataclass(kw_only=True)
class DirectChat:
    _chat: Chat
    _first_user: User
    _second_user: User

    @property
    def chat(self):
        return self._chat

    @staticmethod
    def create(chat: Chat, first_user: User, second_user: User):
        first_user, second_user = sorted([first_user, second_user])
        return DirectChat(_chat=chat, _first_user=first_user, _second_user=second_user)

