from app.application.dtos import ChatDTO, UserDTO
from app.application.services.exceptions import InvalidUsername, NotFoundError
from app.domain.chat import AbstractChatRepository, Chat, ChatType, DirectChat
from app.domain.user import AbstractUserRepository
from app.infrastructure.cache import ChatCache

import logging

logger = logging.getLogger('chat_app')

class ChatService:

    def __init__(self,
                 user_repo_: AbstractUserRepository,
                 chat_repo_: AbstractChatRepository,
                 chat_cache_: ChatCache):
        self._user_repo = user_repo_
        self._chat_repo = chat_repo_
        self._chat_cache = chat_cache_

    async def add_to_direct_chat(self, user: UserDTO, contact_username: str) -> int:
        if contact_username == user.username:
            raise InvalidUsername("Invalid username to add")
        contact = await self._user_repo.get_user_by_username(contact_username)
        if not contact:
            raise NotFoundError("Incorrect contact username")
        current_user = await self._user_repo.get_user_by_username(user.username)

        chat = Chat.create(user.username, {contact, current_user}, ChatType.DIRECT)
        direct_chat = DirectChat.create(chat=chat, first_user=contact, second_user=current_user)

        await self._chat_repo.add_direct_chat(direct_chat)

        async with self._chat_cache as pipe:
            score = int(chat.created_at.timestamp() * 1000)
            pipe.update_list_of_user_chats(chat)
            pipe.update_chat_score(current_user.id, chat, score)

        return chat.id

    async def get_user_chats_by_id(self, user: UserDTO) -> list[dict]:
        chat_ids = await self._chat_cache.get_chat_ids(user.id)

        if not chat_ids:
            chats = await self._chat_repo.get_chats_by_user_id(user.id)
            chat_ids = [c.id for c in chats]

            async with self._chat_cache as pipe:
                for chat in chats:
                    score = int(chat.created_at.timestamp() * 1000)
                    pipe.update_chat_score(user.id, chat, score)

        user_chats = await self._chat_cache.get_chats_previews(chat_ids)
        return user_chats

    async def get_chat_by_id(self, chat_id: int) -> ChatDTO:
        chat = await self._chat_repo.get_chat_by_id(chat_id)
        if not chat:
            raise NotFoundError("Chat with that id wasn't found")

        return ChatDTO.from_entity(chat)

