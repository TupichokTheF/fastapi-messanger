import logging

from fastapi import APIRouter, Body, HTTPException, status

from app.application.services.exceptions import InvalidUsername, NotFoundError
from app.presentation.api.v1.dependencies import ChatServiceDep
from app.presentation.api.v1.dependencies.domain_dep import AuthorizationDep
from app.presentation.api.v1.schemas.responses import (
    AddedToChatResponse,
    UserChatsResponse,
)

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat operation"]
)

logger = logging.getLogger("chat_app")

@chat_router.post(path="/add_direct_chat", response_model=AddedToChatResponse)
async def add_user_to_contact(current_user: AuthorizationDep, chat_service: ChatServiceDep, contact_username: str = Body(embed=True)):
    try:
        chat_id = await chat_service.add_to_direct_chat(current_user, contact_username)
    except (NotFoundError, InvalidUsername) as e:
        logger.warning(f"Failed to create direct chat | first_username={current_user.username}, second_username={contact_username}",
                       extra={"first_username": current_user.username, "second_username": contact_username})
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    logger.info(f"Direct chat created | chat_id={chat_id}", extra = {"chat_id": chat_id})
    return AddedToChatResponse(succeed=True, detail="User added to contact")

@chat_router.get(path="/get_chats_preview", response_model=UserChatsResponse)
async def get_chats_preview(current_user: AuthorizationDep, chat_service: ChatServiceDep):
    chats = await chat_service.get_chats_previews_by_user_id(current_user)

    logger.info(f"Send user chat previews | user_id={current_user.id}", extra={"user_id": current_user.id})
    return UserChatsResponse(succeed=True, detail="Send previews of user chats", chats=chats)


