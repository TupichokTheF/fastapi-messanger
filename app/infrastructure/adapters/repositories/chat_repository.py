from app.domain.chat import Chat, ChatMember, DirectChat
from app.domain.user import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository:

    def __init__(self, session_: AsyncSession):
        self._session = session_

    async def add_direct_chat(self, direct_chat: DirectChat):
        self._session.add(direct_chat)
        await self._session.commit()
        return "Contact added"

    async def get_chats(self, user: User):
        query = select(ChatMember).filter_by(member_id=user.id)
        res = await self._session.execute(query)
        return res.scalars().all()

    async def get_chat_by_name(self, name: str):
        query = select(Chat).filter_by(name=name)
        res = await self._session.execute(query)
        return res.scalars().first()

    async def get_direct_chat_by_members(self, first_user: User, second_user: User):
        first_user, second_user = sorted([first_user, second_user])
        query = select(DirectChat).filter_by(first_user_id=first_user.id, second_user_id=second_user.id)
        res = await self._session.execute(query)
        return res.scalars().first()