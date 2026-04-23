from fastapi import Depends, Cookie, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from app.presentation.api.v1.dependencies import AuthServiceDep
from app.domain.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign_in")

async def get_current_user_ws(auth_service: AuthServiceDep,
                              access_token: str = Query(),
                              refresh_token: str = Cookie()) -> User | None:
    return await auth_service.get_active_user(access_token, refresh_token)

async def get_current_user(auth_service: AuthServiceDep,
                              access_token: str = Depends(oauth2_scheme),
                              refresh_token: str = Cookie()) -> User | None:
    return await auth_service.get_active_user(access_token, refresh_token)


AuthorizationDep = Annotated[User, Depends(get_current_user)]
AuthorizationWsDep = Annotated[User, Depends(get_current_user_ws)]