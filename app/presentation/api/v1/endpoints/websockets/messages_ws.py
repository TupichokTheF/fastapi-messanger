from fastapi import APIRouter, WebSocket, Query

from app.infrastructure.websockets.con_manager import ConManagerDep
from app.core.auth_dep import get_user_by_token
from app.infrastructure.adapters.repositories import UserRepositoryDep

messages_router = APIRouter(prefix="/ws")


@messages_router.websocket("/ws/send_message}")
async def websocket_endpoint(websocket: WebSocket, con_manager: ConManagerDep, current_user):

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Server received: {data}")