from typing import Protocol

from app.application.dtos.message_dto import MessageDTO


class AbstractConnectionManager(Protocol):

    async def send_message(self, message: MessageDTO):
        """Метод для отправки сообщений по WebSocket"""

    async def connect_user(self, chat_id: list[int], user_id: int, websocket):
        """Метод для подключения пользователя"""

    async def disconnect_user(self, user_id: int, websocket):
        """Метод для отключения пользователя"""