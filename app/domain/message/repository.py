from abc import ABC, abstractmethod

from app.domain.message import Message


class AbstractMessageRepo(ABC):

    @abstractmethod
    async def add_message(self, message: Message):
        """Метод для добавления сообщения"""
