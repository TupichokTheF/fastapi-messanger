from app.infrastructure.cache import ChatCache, MessagesCache
from app.domain.message import Message
from app.application.services.exceptions import NotFoundError
from app.application.dtos import UserDTO, ChatDTO, MessageDTO, FilterParamsDTO
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

    async def send_message(self, message_data: MessageDTO, current_user: UserDTO) -> MessageDTO:
        sender = await self._user_repo.get_user_by_username(current_user.username)
        chat = await self._chat_repo.get_chat_by_id(message_data.chat_id)
        if not chat:
            raise NotFoundError("Invalid chat id")
        chat.check_member(sender.id)

        message = Message.create(sender, message_data.text, chat)

        await self._messages_repo.add_message(message)
        async with (self._chat_cache as chat_pipe,
                    self._messages_cache as message_pipe):
            score = int(message.created_at.timestamp() * 1000)
            chat_pipe.update_chat_preview(chat, message)
            for chat_member in chat.members:
                chat_pipe.update_chat_score(chat_member.user.id, chat, score)

            message_pipe.cache_message(message)

        return MessageDTO.from_entity(message)

    async def get_latest_messages_of_chat(self, chat_dto: ChatDTO) -> list[MessageDTO]:
        chat = await self._chat_repo.get_chat_by_id(chat_dto.id)

        latest_messages = await self._messages_cache.get_last_messages_by_chat_id(chat.id)
        if latest_messages:
            return latest_messages

        latest_messages = await self._messages_repo.get_latest_messages_by_chat_id(chat.id)

        async with self._messages_cache as pipe:
            for message in latest_messages:
                pipe.cache_message(message)

        latest_messages = [MessageDTO.from_entity(message) for message in latest_messages]

        return latest_messages

    async def get_messages_from_chat(self, chat: ChatDTO, filter_params: FilterParamsDTO) -> list[MessageDTO]:
        messages = await self._messages_repo.get_messages_from_chat(chat.id, **filter_params.as_dict())

        return [MessageDTO.from_entity(message) for message in messages]


