from app.core.database import SessionDep
from app.schemas.user_schema import UserSignUp
from app.models import User
from app.utils.security import get_password_hash

from fastapi import Depends

from typing import Annotated

from sqlalchemy import select

class UserRepository:

    def __init__(self, session: SessionDep):
        self._session = session

    async def create_user(self, user_data: UserSignUp):
        user_data.password = get_password_hash(user_data.password)
        user = User(**user_data.model_dump())
        self._session.add(user)
        await self._session.commit()
        return "Added"

    async def get_user_by_username(self, username: str):
        query = select(User).filter_by(username=username)
        res = await self._session.execute(query)
        return res.scalars().first()

UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]