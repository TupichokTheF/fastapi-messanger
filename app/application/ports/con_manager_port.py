from abc import ABC, abstractmethod

from app.application.dtos.message_dto import MessageDTO


class AbstractConnectionManager(ABC):

    @abstractmethod
    async def send_message(self, message: MessageDTO):
        """Метод для отправки сообщений по WebSocket"""

    @abstractmethod
    async def connect_user(self, chat_id: list[int], user_id: int, websocket):
        """Метод для подключения пользователя"""

    @abstractmethod
    async def disconnect_user(self, user_id: int, websocket):
        """Метод для отключения пользователя"""