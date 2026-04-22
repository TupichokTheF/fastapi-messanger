from fastapi import APIRouter, WebSocket

from app.infrastructure.websockets.con_manager import ConManagerDep
from app.core.auth_dep import AuthorizationWsDep

messages_router = APIRouter(prefix="/ws")


@messages_router.websocket("/send_message")
async def websocket_endpoint(websocket: WebSocket, con_manager: ConManagerDep, current_user: AuthorizationWsDep):
    await con_manager.connect(current_user.id, websocket)
    data = await websocket.receive_text()
    await websocket.send_text(f"Server received: {current_user.username}")