from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.message import Message

from collections.abc import  Sequence


class MessageRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, message: Message) -> int:
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)

        return message.id

    async def get_latest_messages_by_chat_id(self, chat_id: int) -> Sequence[Message]:
        query = (
            select(Message)
            .filter(Message._chat_id == chat_id)
            .order_by(Message._created_at.desc())
            .limit(50)
        )
        res = await self._session.execute(query)

        return res.scalars().all()

    async def get_messages_from_chat(self, chat_id: int, **filter_params) -> Sequence[Message]:
        query = (select(Message)
                 .filter(Message._chat_id==chat_id)
                 .offset(filter_params['offset'])
                 .limit(filter_params['limit']))
        messages = await self._session.execute(query)

        return messages.scalars().all()