from fastapi import WebSocket

from datetime import datetime
from collections import defaultdict
import json
import logging
import asyncio

from app.infrastructure.database.redis.conn import RedisCon

logger = logging.getLogger("chat_app")

class ConnectionManager:

    def __init__(self):
        self._active_connections: dict[int, set[WebSocket]] = defaultdict(set)
        self._chat_users: dict[int, set[int]] = defaultdict(set)
        self._redis = RedisCon.get_redis()
        self._pubsub = self._redis.pubsub()

    async def init_listening(self):
        await self._pubsub.subscribe("chat:init_sub")
        while True:
            try:
                async for message in self._pubsub.listen():
                    if message["type"] == "message":
                        data = json.loads(message["data"])
                        await self._send_message(data)
            except Exception:
                logger.exception("Redis pub/sub connection failed, retrying")
                await asyncio.sleep(3)

    async def _send_message(self, data: dict):
        users = self._chat_users[int(data["chat_id"])]
        data_to_send = {"chat_id": int(data["chat_id"]),
                        "sender": data["sender"],
                        "message": data["message"],
                        "created_at": datetime.now().timestamp()}
        for user in users:
            if user == int(data["sender_id"]):
                continue
            user_ws = self._active_connections[user]
            for ws in user_ws:
                await ws.send_json(data_to_send)

    async def publish_message(self, message_data: dict):
        channel = f"chat:{message_data['chat_id']}"
        await self._redis.publish(channel, message=json.dumps(message_data))

    async def test(self, chat_id: int):
       await self._pubsub.subscribe(f"chat:{chat_id}")

    async def connect(self, chat_id: int, user_id: int, web_socket: WebSocket):
        await web_socket.accept()
        if chat_id not in self._chat_users:
            await self._pubsub.subscribe(f"chat:{chat_id}")
        self._chat_users[chat_id].add(user_id)
        self._active_connections[user_id].add(web_socket)

    async def disconnect(self, user_id: int, web_socket: WebSocket):
        try:
            self._active_connections[user_id].discard(web_socket)
            for chat in self._chat_users.values():
                chat.discard(user_id)
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

connection_manager = ConnectionManager()
