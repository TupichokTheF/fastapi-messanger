from abc import ABC, abstractmethod

from app.domain.user import User


class AbstractUserRepository(ABC):

    @abstractmethod
    async def create_user(self, user: User) -> int:
        """Метод для добавления пользователя в базу данных"""

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        """Метод для получения User апо его id"""

    @abstractmethod
    async def get_user_by_username(self, raw_username: str) -> User:
        """Метод для получения User апо его username"""
