from fastapi import WebSocket, Depends
from typing import Annotated


class ConnectionManager:

    def __init__(self):
        self._active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, web_socket: WebSocket):
        await web_socket.accept()
        self._active_connections[user_id] = web_socket

    async def disconnect(self, user_id: int, web_socket: WebSocket):
        await web_socket.close(code=1000)
        del self._active_connections[user_id]

    @property
    def active_connections(self):
        return self._active_connections

ConManagerDep = Annotated[ConnectionManager, Depends(ConnectionManager)]