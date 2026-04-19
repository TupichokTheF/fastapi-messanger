from fastapi import Depends, HTTPException, status, Cookie, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import Field
from typing import Annotated

from app.core.settings import settings
from app.infrastructure.adapters.repositories import UserRepositoryDep, TokenRepositoryDep
from app.domain.user import User

import jwt
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign_in")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_rep: UserRepositoryDep):
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

async def check_authorization(token_repo: TokenRepositoryDep,
                              current_user: Annotated[User, Depends(get_current_user)],
                              refresh_token: Annotated[str, Cookie()]
                              ):
    try:
        await token_repo.get_username_by_refresh_token(refresh_token)
    except HTTPException as e:
        raise e
    return current_user

async def get_current_user_ws(token: Annotated[str, Query()], user_rep: UserRepositoryDep):
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

async def check_authorization_ws(token_repo: TokenRepositoryDep,
                              current_user: Annotated[User, Depends(get_current_user_ws)],
                              refresh_token: Annotated[str, Cookie()]
                              ):
    try:
        await token_repo.get_username_by_refresh_token(refresh_token)
    except HTTPException as e:
        raise e
    return current_user

AuthorizationDep = Annotated[User, Depends(check_authorization)]
AuthorizationWsDep = Annotated[User, Depends(check_authorization_ws)]