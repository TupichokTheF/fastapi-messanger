from fastapi import WebSocket, Depends
from typing import Annotated

from app.domain.user import User


class ConnectionManager:

    def __init__(self):
        self._active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, web_socket: WebSocket):
        await web_socket.accept()
        self._active_connections[user_id] = web_socket

    async def disconnect(self, user_id: int, web_socket: WebSocket):
        try:
            del self._active_connections[user_id]
            await web_socket.close(code=1000)
        except RuntimeError:
            pass

    def get_ws_by_user(self, user_id: int) -> WebSocket:
        return self._active_connections[user_id]

    def is_online(self, user_id: int):
        return user_id in self._active_connections

    @property
    def active_connections(self):
        return self._active_connections