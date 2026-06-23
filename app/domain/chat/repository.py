from abc import abstractmethod, ABC

from app.domain.chat import DirectChat, Chat, ChatMember
from app.domain.user import User


class AbstractChatRepository(ABC):

    @abstractmethod
    async def add_direct_chat(self, direct_chat: DirectChat) -> bool:
        """Метод для создания личного чата"""

    @abstractmethod
    async def get_chats_by_user_id(self, user_id: int) -> list[Chat]:
        """Метод для получения всех чатов пользователя по его id"""

    @abstractmethod
    async def get_chat_by_id(self, chat_id: int) -> Chat:
        """Метод для получения чата по его id"""

    @abstractmethod
    async def get_direct_chat_by_members(self, first_user: User, second_user: User) -> DirectChat:
        """Метод для получения личного чата по его участникам"""
