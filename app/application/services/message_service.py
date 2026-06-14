from app.infrastructure.adapters.repositories import UserRepository, MessageRepository, ChatRepository
from app.infrastructure.cache import ChatCache
from app.application.services import UserService
from app.domain.user import User
from app.domain.message import Message
from app.application.services.exceptions import NotFoundError


class MessageService:

    def __init__(self, messages_repo: MessageRepository,
                 user_repo: UserRepository,
                 chat_cache_: ChatCache,
                 chat_repo_: ChatRepository):
        self._messages_repo = messages_repo
        self._user_repo = user_repo
        self._chat_cache = chat_cache_
        self._chat_repo = chat_repo_

    async def send_direct_message(self, message_data: dict, current_user: User):
        receiver = await self._user_repo.get_user_by_username(message_data["receiver"])
        if not receiver:
            raise NotFoundError("Invalid username")
        direct_chat = await self._chat_repo.get_direct_chat_by_members(current_user, receiver)
        message = Message.create(current_user, message_data["message"], direct_chat.chat)
        await self._messages_repo.add_message(message)
        async with self._chat_cache as pipe:
            pipe.update_chat_preview(direct_chat.chat, message)
            pipe.update_chat_score(current_user.id, direct_chat.chat)
            pipe.update_chat_score(receiver.id, direct_chat.chat)
        return message, receiver


    async def get_latest_messages(self, user: User):
        pass


