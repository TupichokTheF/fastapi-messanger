from typing import Protocol

from app.domain.message import Message


class AbstractMessageRepo(Protocol):

    async def add_message(self, message: Message):
        """Метод для добавления сообщения"""

    async def get_latest_messages_by_chat_id(self, chat_id: int):
        """Метод для получения последних 50 сообщений из БД, в случае, если в Redis их не окажется"""