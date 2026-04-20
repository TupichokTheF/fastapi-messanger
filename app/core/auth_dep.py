from fastapi import Depends, HTTPException, status, Cookie, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from app.core.settings import settings
from app.infrastructure.adapters.repositories import UserRepositoryDep, TokenRepositoryDep, UserRepository, TokenRepository
from app.domain.user import User

import jwt
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign_in")


async def get_user_by_token(token: str, user_rep: UserRepository) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM_OF_CIFER])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await user_rep.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_ws(user_rep: UserRepositoryDep, access_token: str = Query()) -> User:
    return await get_user_by_token(access_token, user_rep)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_rep: UserRepositoryDep) -> User:
    return await get_user_by_token(token, user_rep)


AuthorizationDep = Annotated[User, Depends(get_current_user)]
AuthorizationWsDep = Annotated[User, Depends(get_current_user_ws)]