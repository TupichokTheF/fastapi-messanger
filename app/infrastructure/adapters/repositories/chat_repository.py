from app.domain.chat import Chat, ChatMember, DirectChat, AbstractChatRepository
from app.domain.user import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository(AbstractChatRepository):

    def __init__(self, session_: AsyncSession):
        self._session = session_

    async def add_direct_chat(self, direct_chat: DirectChat) -> bool:
        self._session.add(direct_chat)
        await self._session.commit()
        return True

    async def get_chats_by_user_id(self, user_id: int):
        query = (select(Chat)
                 .join(ChatMember, ChatMember.chat_id == Chat.id)
                 .where(ChatMember.member_id == user_id))
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_chat_by_id(self, chat_id: int):
        query = select(Chat).filter_by(id=chat_id)
        res = await self._session.execute(query)
        return res.scalars().first()

    async def get_direct_chat_by_members(self, first_user: User, second_user: User):
        first_user, second_user = sorted([first_user, second_user])
        query = select(DirectChat).filter_by(first_user_id=first_user.id, second_user_id=second_user.id)
        res = await self._session.execute(query)
        return res.scalars().first()