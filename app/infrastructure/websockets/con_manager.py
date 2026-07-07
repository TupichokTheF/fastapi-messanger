from fastapi import WebSocket

from app.domain.message import MessageSentEvent
from app.application.dtos import MessageDTO
from app.infrastructure.messaging.redis import message_bus, MessageBus
from app.infrastructure.websockets import connection_list, ConnectionList

import json


class ConnectionManager:

    def __init__(self):
        self._list_of_connections: ConnectionList = connection_list
        self._message_bus: MessageBus = message_bus

    async def send_message(self, message: MessageDTO):
        event = MessageSentEvent(**message.as_dict())
        await self._message_bus.publish_event(event)

    async def connect_user(self, chat_ids: list[int], user_id: int, websocket: WebSocket):
        await websocket.accept()

        self._list_of_connections.add_user_to_active_connections(user_id, websocket)
        self._list_of_connections.add_user_to_chats(user_id, chat_ids)

    async def disconnect_user(self, user_id: int, websocket: WebSocket):
        self._list_of_connections.disconnect_user(user_id, websocket)

    async def deliver_message(self, message: MessageSentEvent):
        users_websockets = self._list_of_connections.get_websockets_by_chat_id(message.chat_id)
        sender_ws = self._list_of_connections.get_websocket_by_user_id(message.sender_id)

        for user_ws in users_websockets:
            if user_ws in sender_ws:
                continue

            await user_ws.send_json(message.as_dict())

connection_manager: ConnectionManager = ConnectionManager()
