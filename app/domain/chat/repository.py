from typing import Protocol

from app.domain.chat import Chat, DirectChat
from app.domain.user import User


class AbstractChatRepository(Protocol):

    async def add_direct_chat(self, direct_chat: DirectChat) -> bool:
        """Метод для создания личного чата"""

    async def get_chats_by_user_id(self, user_id: int) -> list[Chat]:
        """Метод для получения всех чатов пользователя по его id"""

    async def get_chat_by_id(self, chat_id: int) -> Chat:
        """Метод для получения чата по его id"""

    async def get_direct_chat_by_members(self, first_user: User, second_user: User) -> DirectChat:
        """Метод для получения личного чата по его участникам"""
