from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.message import AbstractMessageRepo, Message


class MessageRepository(AbstractMessageRepo):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, message: Message):
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message.id

    async def get_latest_messages_by_chat_id(self, chat_id: int):
        query = select(Message).