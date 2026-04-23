from app.presentation.api.v1.schemas.message_schema import MessageBase
from app.domain.message.entities import Message
from app.domain.message.value_objects import MessageText

from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepo:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, raw_message: MessageBase):
        message = Message.create(spender=raw_message.spender, text=MessageText(raw_message.text))
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message.id