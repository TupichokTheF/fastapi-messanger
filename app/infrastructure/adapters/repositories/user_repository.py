from app.infrastructure.database.postgresql.db import SessionDep
from app.core.schemas.user_schema import UserSignUp
from app.domain.user.entities import User
from app.domain.user.value_objects import UserPassword, UserEmail, UserUsername

from fastapi import Depends

from typing import Annotated

from sqlalchemy import select

class UserRepository:

    def __init__(self, session: SessionDep):
        self._session = session

    async def create_user(self, user_data: UserSignUp) -> int:
        user = User(username=UserUsername(user_data.username),
                    email=UserEmail(user_data.email),
                    password=UserPassword.create(user_data.password))
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user.id

    async def get_user_by_username(self, raw_username: str) -> User:
        username = UserUsername(raw_username)
        query = select(User).filter_by(username=username)
        res = await self._session.execute(query)
        return res.scalars().first()

UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]