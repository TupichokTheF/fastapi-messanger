from app.infrastructure.adapters.repositories.user_repository import UserRepository
from app.application.services.exceptions import NotFoundError
from app.domain.user import User, Contact
from app.domain.user.value_objects import UserUsername
from app.infrastructure.cache import ContactsCache


class UserService:

    def __init__(self, user_repo: UserRepository, contacts_cache_: ContactsCache):
        self._user_repo = user_repo
        self._contacts_cache = contacts_cache_

    async def create_user(self, user_data: User):
        return await self._user_repo.create_user(user_data)

    async def add_to_contact(self, user: User, contact_username: str) -> bool:
        contact_user = await self._user_repo.get_user_by_username(contact_username)
        if not contact_user:
            raise NotFoundError("Incorrect contact username")
        contact = Contact.create(user, contact_user)
        await self._contacts_cache.add_contact(contact)
        await self._user_repo.add_contact(contact)
        return True

    async def get_contacts(self, user: User) -> list[UserUsername]:
        contacts_order = await self._contacts_cache.get_contacts_ids(user)
        user_contacts = await self._user_repo.get_contacts(user)
        contacts = {contact_.contact.id: contact_.contact.raw_username for contact_ in user_contacts}
        return [contacts[contact_id] for contact_id in contacts_order]
