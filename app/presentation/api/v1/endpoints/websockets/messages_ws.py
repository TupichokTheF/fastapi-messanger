from fastapi import APIRouter, WebSocket, Cookie

from app.presentation.api.v1.dependencies import AuthorizationWsDep, ConManagerDep, MessageServiceDep, ChatServiceDep
from app.presentation.api.v1.schemas import ErrorResponse, MessageSendResponse
from app.application.services.exceptions import NotFoundError
from app.domain.message.exceptions import EmptyMessage

messages_ws = APIRouter(
    tags = ["Websocket operations with messages"],
    prefix="/ws",
)


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
            user_data = await websocket.receive_json()
            try:
                message = await message_service.send_direct_message(user_data, current_user)
            except (EmptyMessage, NotFoundError) as e:
                await websocket.send_json(ErrorResponse(detail=str(e)).model_dump(mode="json"))
                continue
            await con_manager.send_message(message)
            await websocket.send_json(MessageSendResponse(succeed=True,
                                                          detail="Message send",
                                                          created_at=message.created_at).model_dump(mode="json"))
    except Exception as e:
        pass
    finally:
        await con_manager.disconnect_user(current_user.id, websocket)



