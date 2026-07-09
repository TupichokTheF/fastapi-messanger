from typing import Protocol
from collections.abc import Sequence

from app.domain.message import Message


class AbstractMessageRepo(Protocol):

    async def add_message(self, message: Message) -> int:
        """Метод для добавления сообщения"""

    async def get_latest_messages_by_chat_id(self, chat_id: int) -> Sequence[Message]:
        """Метод для получения последних 50 сообщений из БД, в случае, если в Redis их не окажется"""

    async def get_messages_from_chat(self, chat_id: int, **filter_params) -> Sequence[Message]:
        """Метод для получения сообщений из чата с заданными фильтрационными параметрами"""