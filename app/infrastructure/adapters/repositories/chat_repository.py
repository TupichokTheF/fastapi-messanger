from app.domain.chat import Chat, ChatMember, DirectChat, AbstractChatRepository
from app.domain.user import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository(AbstractChatRepository):

    def __init__(self, session_: AsyncSession):
        self._session = session_

    async def add_direct_chat(self, direct_chat: DirectChat):
        self._session.add(direct_chat)
        await self._session.commit()
        return "Contact added"

    async def get_chats_by_user_id(self, user_id: int):
        get_chat_ids_query = select(ChatMember).filter_by(member_id=user_id)
        chat_ids = await self._session.execute(get_chat_ids_query)
        chat_ids = chat_ids.scalars().all()

        chats = [self.get_chat_by_id(chat_id) for chat_id in chat_ids]
        return chats

    async def get_chat_by_id(self, chat_id: int):
        query = select(Chat).filter_by(id=chat_id)
        res = await self._session.execute(query)
        return res.scalars().first()

    async def get_direct_chat_by_members(self, first_user: User, second_user: User):
        first_user, second_user = sorted([first_user, second_user])
        query = select(DirectChat).filter_by(first_user_id=first_user.id, second_user_id=second_user.id)
        res = await self._session.execute(query)
        return res.scalars().first()