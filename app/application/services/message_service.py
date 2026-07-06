from app.infrastructure.cache import ChatCache, MessagesCache
from app.domain.message import Message
from app.application.services.exceptions import NotFoundError
from app.application.dtos import UserDTO, ChatDTO, MessageDTO
from app.domain.chat import AbstractChatRepository
from app.domain.user import AbstractUserRepository
from app.domain.message import AbstractMessageRepo


class MessageService:

    def __init__(self, messages_repo: AbstractMessageRepo,
                 user_repo: AbstractUserRepository,
                 chat_cache_: ChatCache,
                 chat_repo_: AbstractChatRepository,
                 messages_cache_: MessagesCache):
        self._messages_repo = messages_repo
        self._user_repo = user_repo
        self._chat_cache = chat_cache_
        self._chat_repo = chat_repo_
        self._messages_cache = messages_cache_

    async def send_direct_message(self, message_data: dict, current_user: UserDTO) -> MessageDTO:
        sender = await self._user_repo.get_user_by_username(current_user.username)
        receiver = await self._user_repo.get_user_by_username(message_data["receiver"])
        if not receiver:
            raise NotFoundError("Invalid username")

        direct_chat = await self._chat_repo.get_direct_chat_by_members(sender, receiver)
        message = Message.create(sender, message_data["message"], direct_chat.chat)

        await self._messages_repo.add_message(message)
        async with (self._chat_cache as chat_pipe,
                    self._messages_cache as message_pipe):
            score = int(direct_chat.chat.created_at.timestamp() * 1000)
            chat_pipe.update_chat_preview(direct_chat.chat, message)
            chat_pipe.update_chat_score(sender.id, direct_chat.chat, score)
            chat_pipe.update_chat_score(receiver.id, direct_chat.chat, score)

            message_pipe.cache_message(message)

        return MessageDTO.from_entity(message)

    async def get_latest_messages_of_chat(self, user_dto: UserDTO, chat_dto: ChatDTO):
        chat = await self._chat_repo.get_chat_by_id(chat_dto.id)
        user = await self._user_repo.get_user_by_id(user_dto.id)

        chat.check_member(user)
        latest_messages = await self._messages_cache.get_last_messages_by_chat_id(chat.id)

        return latest_messages


