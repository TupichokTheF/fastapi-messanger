from app.domain.message import Message, AbstractMessageRepo

from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepository(AbstractMessageRepo):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, message: Message):
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message.id
