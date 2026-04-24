from app.domain.message.entities import Message, MessageReceiver

from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepo:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, message: Message):
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message.id

    async def add_message_receiver(self, message_receiver: MessageReceiver):
        self._session.add(message_receiver)
        await self._session.commit()
        await self._session.refresh(message_receiver)
        return message_receiver