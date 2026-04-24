from app.infrastructure.adapters.repositories import MessageRepo, UserRepository
from app.domain.user import User
from app.domain.message import Message, MessageReceiver
from app.application.services.exceptions import NotFoundError


class MessageService:

    def __init__(self, messages_repo: MessageRepo, user_repo: UserRepository):
        self._messages_repo = messages_repo
        self._user_repo = user_repo

    async def send_message(self, message_data: dict, current_user: User):
        message = Message.create(current_user, message_data["text"])
        receiver = await self._user_repo.get_user_by_username(message_data["receiver"])
        if not receiver:
            raise NotFoundError("Invalid username")
        message_receiver = MessageReceiver.create(message=message, receiver=receiver)
        await self._messages_repo.add_message(message)
        await self._messages_repo.add_message_receiver(message_receiver)

        return message_receiver

