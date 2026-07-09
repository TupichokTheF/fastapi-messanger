from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Query, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer

from app.application.dtos import ChatDTO, UserDTO, FilterParamsDTO
from app.application.services.exceptions import NotFoundError, WrongTokenError
from app.presentation.api.v1.dependencies.services_deps import AuthServiceDep, ChatServiceDep
from app.presentation.api.v1.schemas.common import FilterParams

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign_in")

async def get_current_user_ws(websocket: WebSocket,
                              auth_service: AuthServiceDep,
                              access_token: str = Query(),
                              refresh_token: str = Cookie()) -> UserDTO | None:
    try:
        return await auth_service.get_active_user(access_token, refresh_token)
    except (WrongTokenError, NotFoundError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)

async def get_current_user(auth_service: AuthServiceDep,
                           access_token: str = Depends(oauth2_scheme),
                           refresh_token: str = Cookie()) -> UserDTO | None:
    try:
        return await auth_service.get_active_user(access_token, refresh_token)
    except (WrongTokenError, NotFoundError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_chat_by_id(chat_service: ChatServiceDep,
                         current_user: UserDTO = Depends(get_current_user),
                         chat_id: int = Query()) -> ChatDTO:
    try:
        chat = await chat_service.get_chat_by_id(chat_id, current_user)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )

    return chat

async def get_filter_params(filter_params: FilterParams):
    return FilterParamsDTO(**filter_params.model_dump())

ChatDep = Annotated[ChatDTO, Depends(get_chat_by_id)]
AuthorizationDep = Annotated[UserDTO, Depends(get_current_user)]
AuthorizationWsDep = Annotated[UserDTO, Depends(get_current_user_ws)]
FilterParamsDep = Annotated[FilterParamsDTO, Depends(get_filter_params)]
