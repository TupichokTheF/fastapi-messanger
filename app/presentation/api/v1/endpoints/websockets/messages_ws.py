from fastapi import APIRouter, WebSocket

from app.presentation.api.v1.dependencies import AuthorizationWsDep, ConManagerDep, MessageServiceDep, ChatServiceDep
from app.presentation.api.v1.schemas import ErrorResponse, MessageSendResponse
from app.application.services.exceptions import NotFoundError
from app.application.dtos import MessageDTO
from app.domain.message.exceptions import EmptyMessage

import logging

messages_ws = APIRouter(
    tags = ["Websocket operations with messages"],
    prefix="/ws",
)

logger = logging.getLogger('chat_app')

@messages_ws.websocket("/send_message")
async def websocket_endpoint(websocket: WebSocket,
                             con_manager: ConManagerDep,
                             message_service: MessageServiceDep,
                             chat_service: ChatServiceDep,
                             current_user: AuthorizationWsDep):
    chats = await chat_service.get_user_chats_by_user_id(current_user.id)
    chat_ids = [chat.id for chat in chats]
    await con_manager.connect_user(chat_ids, current_user.id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = MessageDTO(**data)
            try:
                message = await message_service.send_message(message, current_user)
            except (EmptyMessage, NotFoundError) as e:
                await websocket.send_json(ErrorResponse(detail=str(e)).model_dump(mode="json"))
                continue
            await con_manager.send_message(message)
            await websocket.send_json(MessageSendResponse(succeed=True,
                                                          detail="Message send",
                                                          created_at=message.created_at_timestamp_ms).model_dump(mode="json"))
    except Exception:
        logger.exception(f"Unexpected WS error | user_id={current_user.id}")
    finally:
        await con_manager.disconnect_user(current_user.id, websocket)



