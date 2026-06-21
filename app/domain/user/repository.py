from abc import ABC, abstractmethod

from app.domain.user import User

class AbstractUserRepository(ABC):

    @abstractmethod
    async def create_user(self, user: User) -> int:
        pass

    @abstractmethod
    async def get_user_by_username(self, raw_username: str) -> User:
        pass