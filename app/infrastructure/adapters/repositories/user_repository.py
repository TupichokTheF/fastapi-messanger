from app.infrastructure.database.postgresql.db import SessionDep
from app.core.schemas.user_schema import UserSignUp
from app.domain.user.entities import User, Contact
from app.domain.user.value_objects import UserPassword, UserEmail, UserUsername

from fastapi import Depends

from typing import Annotated

from sqlalchemy import select

class UserRepository:

    def __init__(self, session: SessionDep):
        self._session = session

    async def create_user(self, user_data: UserSignUp) -> int:
        user = User.create(UserUsername(user_data.username),
                           UserEmail(user_data.email),
                           UserPassword.create(user_data.password))
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

    async def get_contacts(self, user: User):
        query = select(Contact).filter_by(user_id=user.id)
        res = await self._session.execute(query)
        return res.scalars().all()

UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]