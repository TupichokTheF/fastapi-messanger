import logging

from anyio import current_effective_deadline
from fastapi import APIRouter

from app.presentation.api.v1.dependencies import (
    AuthorizationDep,
    ChatDep,
    MessageServiceDep,
    FilterParamsDep
)
from app.presentation.api.v1.schemas.responses import ChatMessages


messages_router = APIRouter(
    tags = ["HTTP operations with messages"],
    prefix = "/message"
)

logger = logging.getLogger("chat_app")

@messages_router.get("/get_latest", response_model=ChatMessages)
async def get_latest_messages(current_user: AuthorizationDep, chat: ChatDep, messages_service: MessageServiceDep):
    latest_messages = await messages_service.get_latest_messages_of_chat(chat)

    logger.info(f"Send the fifty latest messages of chat | chat_id={chat.id}, user_id={current_user.id}",
                extra={"chat_id": chat.id, "user_id": current_user.id})
    return ChatMessages(succeed=True,
                        detail="Send the fifty latest messages of chat",
                        messages=latest_messages)


@messages_router.get("/get_messages", response_model=ChatMessages)
async def get_messages_from_chat(current_user: AuthorizationDep,
                                 chat: ChatDep,
                                 messages_service: MessageServiceDep,
                                 filter_params: FilterParamsDep):
    messages = await messages_service.get_messages_from_chat(chat, filter_params)

    logger.info(f"Send filtered list of messages from chat | chat_id={chat.id}, user_id={current_user.id}",
                extra={'chat_id': chat.id, 'user_id': current_user.id})
    return ChatMessages(
        succeed=True,
        detail="Send the filtered list of messages",
        messages=messages
    )


