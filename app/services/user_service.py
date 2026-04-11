from app.repositories.user_repository import UserRepositoryDep
from app.repositories.token_repository import TokenRepositoryDep
from app.schemas.user_schema import UserSignUp, UserSignIn
from app.utils.security import verify_password
from app.core.settings import settings

from fastapi import Depends

from typing import Annotated
from datetime import timedelta, timezone, datetime
import jwt

class UserService:

    def __init__(self, user_repo: UserRepositoryDep, token_repo: TokenRepositoryDep):
        self._user_repo = user_repo
        self._token_repo = token_repo

    async def create_user(self, user_data: UserSignUp):
        return await self._user_repo.create_user(user_data)

    async def authenticate_user(self, user_: UserSignIn):
        user = await self._user_repo.get_user_by_username(user_.username)
        if not user:
            return False
        if not verify_password(user_.password, user.password):
            return False
        return user

    async def generate_refresh_token(self, data: dict):
        encoded_jwt = await self.generate_token(data, settings.REFRESH_TOKEN_EXPIRES)
        await self._token_repo.add_refresh_token(encoded_jwt, data["sub"])
        return encoded_jwt

    async def generate_token(self, data: dict, expires_delta: timedelta | None = settings.ACCESS_TOKEN_EXPIRES):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM_OF_CIFER)
        return encoded_jwt

UserServiceDep = Annotated[UserService, Depends(UserService)]