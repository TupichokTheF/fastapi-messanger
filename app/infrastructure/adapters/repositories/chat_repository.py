from app.domain.chat import Chat, ChatMember
from app.domain.user import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository:

    def __init__(self, session_: AsyncSession):
        self._session = session_

    async def add_to_chat(self, chat: Chat):
        self._session.add(chat)
        await self._session.commit()
        return "Contact added"

    async def get_chats(self, user: User):
        query = select(ChatMember).filter_by(user_id=user.id)
        res = await self._session.execute(query)
        return res.scalars().all()