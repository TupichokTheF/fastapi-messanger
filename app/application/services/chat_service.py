from app.infrastructure.adapters.repositories import UserRepository, ChatRepository
from app.infrastructure.cache import ChatCache
from app.domain.user import User
from app.domain.chat import Chat, ChatType, DirectChat
from app.application.services.exceptions import NotFoundError, InvalidUsername, AlreadyExistError


class ChatService:

    def __init__(self, user_repo_: UserRepository, chat_repo_: ChatRepository, chat_cache_: ChatCache):
        self._user_repo = user_repo_
        self._chat_repo = chat_repo_
        self._chat_cache = chat_cache_

    async def add_to_direct_chat(self, user: User, contact_username: str) -> bool:
        if contact_username == user.username:
            raise InvalidUsername("Invalid username to add")
        contact_user = await self._user_repo.get_user_by_username(contact_username)
        if not contact_user:
            raise NotFoundError("Incorrect contact username")
        if direct_chat := await self._chat_repo.get_direct_chat_by_members(user, contact_user):
            await self._chat_cache.update_chat_score(user, direct_chat.chat)
            raise AlreadyExistError("Direct chat with those members already exist")
        chat = Chat.create(user.username, {contact_user, user}, ChatType.DIRECT)
        direct_chat = DirectChat.create(chat=chat, first_user=user, second_user=contact_user)
        await self._chat_repo.add_direct_chat(direct_chat)
        await self._chat_cache.update_user_chats(chat)
        await self._chat_cache.update_chat_score(user, chat)
        return True

    async def get_chats(self, user: User) -> list[dict]:
        chat_ids = await self._chat_cache.get_chat_ids(user)
        user_chats = await self._chat_cache.get_chats_previews(chat_ids)
        return user_chats

