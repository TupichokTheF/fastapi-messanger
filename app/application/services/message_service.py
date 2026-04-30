from app.infrastructure.adapters.repositories import MessageRepo, UserRepository
from app.infrastructure.cache import ContactsCache
from app.application.services import UserService
from app.domain.user import User, Contact
from app.domain.message import Message, MessageReceiver
from app.application.services.exceptions import NotFoundError


class MessageService:

    def __init__(self, messages_repo: MessageRepo, user_repo: UserRepository, contacts_cache_: ContactsCache, user_service_: UserService):
        self._messages_repo = messages_repo
        self._user_repo = user_repo
        self._contacts_cache = contacts_cache_
        self._user_service = user_service_

    async def send_message(self, message_data: dict, current_user: User):
        message = Message.create(current_user, message_data["text"])
        receiver = await self._user_repo.get_user_by_username(message_data["receiver"])
        if not receiver:
            raise NotFoundError("Invalid username")
        if not await self._user_repo.find_user_contact_by_id(receiver, current_user.id):
            await self._user_service.add_to_contact(receiver, current_user.username)
        message_receiver = MessageReceiver.create(message=message, receiver=receiver)
        await self._contacts_cache.update_contact_score(message_receiver)
        await self._messages_repo.add_message(message)
        await self._messages_repo.add_message_receiver(message_receiver)

        return message_receiver

