from app.infrastructure.adapters.repositories import UserRepository, ChatRepository
from app.domain.user import User
from app.domain.chat import Chat, ChatType
from app.application.services.exceptions import NotFoundError, InvalidUsername


class ChatService:

    def __init__(self, user_repo_: UserRepository, chat_repo_: ChatRepository):
        self._user_repo = user_repo_
        self._chat_repo = chat_repo_

    async def add_to_contact(self, user: User, contact_username: str) -> bool:
        if contact_username == user.username:
            raise InvalidUsername("Invalid username to add")
        contact_user = await self._user_repo.get_user_by_username(contact_username)
        if not contact_user:
            raise NotFoundError("Incorrect contact username")
        chat = Chat.create(user.username, {user}, ChatType.DIRECT)
        #await self._contacts_cache.add_contact(contact)
        await self._chat_repo.add_to_chat(chat)
        return True

    async def get_chats(self, user: User):
        #contacts_order = await self._contacts_cache.get_contacts_ids(user)
        user_chats = await self._chat_repo.get_chats(user)
        #contacts = {contact_.contact.id: contact_.contact.raw_username for contact_ in user_contacts}
        #return [contacts[contact_id] for contact_id in contacts_order]
        return user_chats