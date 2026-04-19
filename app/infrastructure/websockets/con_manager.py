from fastapi import WebSocket, Depends
from typing import Annotated


class ConnectionManager:

    def __init__(self):
        self._active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, web_socket: WebSocket):
        await web_socket.accept()
        self._active_connections[user_id] = web_socket

ConManagerDep = Annotated[ConnectionManager, Depends(ConnectionManager)]