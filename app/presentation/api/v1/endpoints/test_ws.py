from fastapi import APIRouter, WebSocket
from app.core.auth_dep import AuthorizationWsDep
from app.infrastructure.websockets.con_manager import ConManagerDep

test_router = APIRouter(prefix="/ws")


@test_router.websocket("/auth")
async def websockets_auth(user: AuthorizationWsDep, websocket: WebSocket, con_manager: ConManagerDep):
    await con_manager.connect(user.id, websocket)
    while True:
        data = await websocket.receive_text()


@test_router.websocket("/ws/send_message")
async def websocket_endpoint(websocket: WebSocket, con_manager: ConManagerDep, receiver_id: int):
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Server received: {data}")