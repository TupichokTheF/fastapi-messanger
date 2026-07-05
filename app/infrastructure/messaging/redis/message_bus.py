from app.domain.base import BaseEvent
from app.domain.message import MessageReceivedEvent
from app.infrastructure.database.redis.conn import RedisCon

from redis.asyncio import Redis

import asyncio
import json
import logging

logger = logging.getLogger('chat_app')

class MessageBus:

    def __init__(self, redis_: Redis):
        self._redis = redis_
        self._pubsub = self._redis.pubsub()

    async def start_listen(self) -> BaseEvent:
        while True:
            try:
                async for message in self._pubsub.listen():
                    if message["type"] == "message":
                        data = json.loads(message["data"])
                        return MessageReceivedEvent(**data)
            except Exception:
                logger.exception("Redis pub/sub connection failed, retrying")
                await asyncio.sleep(3)
        
    async def publish_message(self, channel: str, message_data: dict) -> None:
        await self._redis.publish(channel, message=json.dumps(message_data))

    async def subscribe(self, channel: str) -> None:
        await self._pubsub.subscribe(channel)

message_bus = MessageBus(RedisCon.get_redis())