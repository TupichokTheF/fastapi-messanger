from app.domain.user.entities import User, Contact
from app.domain.user.value_objects import UserPassword, UserEmail, UserUsername

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, user: User) -> int:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user.id

    async def get_user_by_username(self, raw_username: str) -> User:
        username = UserUsername(raw_username)
        query = select(User).filter_by(_username=username)
        res = await self._session.execute(query)
        return res.scalars().first()

    async def add_contact(self, contact: Contact):
        self._session.add(contact)
        await self._session.commit()
        return "Contact added"

    async def get_contacts(self, user: User) -> list[Contact]:
        query = select(Contact).filter_by(user_id=user.id)
        res = await self._session.execute(query)
        return res.scalars().all()

    async def find_user_contact_by_id(self, user: User, contact_id: int):
        query = select(Contact).filter_by(user_id=user.id, contact_id=contact_id)
        res = await self._session.execute(query)
        return res.scalars().one_or_none()
