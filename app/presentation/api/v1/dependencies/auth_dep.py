from fastapi import Depends, Cookie, Query, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from app.presentation.api.v1.dependencies import AuthServiceDep
from app.application.dtos import UserDTO


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign_in")

async def get_current_user_ws(auth_service: AuthServiceDep,
                              access_token: str = Query(),
                              refresh_token: str = Cookie()) -> UserDTO | None:
    try:
        return await auth_service.get_active_user(access_token, refresh_token)
    except Exception as e:
        raise e

async def get_current_user(auth_service: AuthServiceDep,
                              access_token: str = Depends(oauth2_scheme),
                              refresh_token: str = Cookie()) -> UserDTO | None:
    try:
        return await auth_service.get_active_user(access_token, refresh_token)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


AuthorizationDep = Annotated[UserDTO, Depends(get_current_user)]
AuthorizationWsDep = Annotated[UserDTO, Depends(get_current_user_ws)]