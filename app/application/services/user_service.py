from app.infrastructure.adapters.repositories.user_repository import UserRepository
from app.infrastructure.adapters.repositories.token_repository import TokenRepository
from app.application.services.exceptions import NotFoundError
from app.domain.user import User, Contact
from app.domain.user.value_objects import UserUsername


class UserService:

    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self._user_repo = user_repo
        self._token_repo = token_repo

    async def create_user(self, user_data: User):
        return await self._user_repo.create_user(user_data)

    async def add_to_contact(self, user: User, contact_username: str) -> bool:
        contact_user = await self._user_repo.get_user_by_username(contact_username)
        if not contact_user:
            raise NotFoundError("Incorrect contact username")
        contact = Contact.create(user, contact_user)
        await self._user_repo.add_contact(contact)
        return True

    async def get_contacts(self, user: User) -> list[UserUsername]:
        contacts = await self._user_repo.get_contacts(user)
        contacts_username = [UserUsername(contact.contact.username) for contact in contacts]
        return contacts_username
