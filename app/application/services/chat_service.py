from app.infrastructure.adapters.repositories import UserRepository, ChatRepository
from app.infrastructure.cache import ChatCache
from app.domain.user import User
from app.domain.chat import Chat, ChatType, DirectChat
from app.application.services.exceptions import NotFoundError, InvalidUsername, AlreadyExistError
from app.application.dtos import UserDTO


class ChatService:

    def __init__(self, user_repo_: UserRepository, chat_repo_: ChatRepository, chat_cache_: ChatCache):
        self._user_repo = user_repo_
        self._chat_repo = chat_repo_
        self._chat_cache = chat_cache_

    async def add_to_direct_chat(self, user: UserDTO, contact_username: str) -> bool:
        if contact_username == user.username:
            raise InvalidUsername("Invalid username to add")
        first_member = await self._user_repo.get_user_by_username(contact_username)
        if not first_member:
            raise NotFoundError("Incorrect contact username")
        second_member = await self._user_repo.get_user_by_username(user.username)

        if direct_chat := await self._chat_repo.get_direct_chat_by_members(first_member, second_member):
            async with self._chat_cache as pipe:
                pipe.update_chat_score(user.id, direct_chat.chat)
            raise AlreadyExistError("Direct chat with those members already exist")

        chat = Chat.create(user.username, {first_member, second_member}, ChatType.DIRECT)
        direct_chat = DirectChat.create(chat=chat, first_user=first_member, second_user=second_member)

        await self._chat_repo.add_direct_chat(direct_chat)
        async with self._chat_cache as pipe:
            pipe.update_user_chats(chat)
            pipe.update_chat_score(second_member.id, chat)

        return True

    async def get_chats(self, user: UserDTO) -> list[dict]:
        chat_ids = await self._chat_cache.get_chat_ids(user.id)
        if not chat_ids:
            chats = await self._chat_repo.get_chats(user.id)
            chat_ids = [c.chat_id for c in chats]
            async with self._chat_cache as pipe:
                for chat in chats:
                    pipe.update_chat_score(user.id, chat)
        user_chats = await self._chat_cache.get_chats_previews(chat_ids)
        return user_chats

