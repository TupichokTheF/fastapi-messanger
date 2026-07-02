from fastapi import APIRouter, Body

from app.presentation.api.v1.dependencies import AuthorizationDep, MessageServiceDep, ChatDep
from app.presentation.api.v1.schemas.responses import ChatLatestMessages

import logging

messages_router = APIRouter(
    tags = ["HTTP operations with messages"],
    prefix = "/message"
)

logger = logging.getLogger("chat_app")

@messages_router.get("/get_latest", response_model=ChatLatestMessages)
async def get_latest_messages(current_user: AuthorizationDep, chat: ChatDep, messages_service: MessageServiceDep):
    latest_messages = await messages_service.get_latest_messages_of_chat(current_user, chat)

    logger.info(f"Send the fifty latest messages of chat | chat_id={chat.id}, user_id={current_user.id}",
                extra={"chat_id": chat.id, "user_id": current_user.id})
    return ChatLatestMessages(succeed=True,
                              detail="Send the fifty latest messages of chat",
                              messages=latest_messages)
