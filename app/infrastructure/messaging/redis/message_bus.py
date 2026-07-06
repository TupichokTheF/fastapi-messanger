from typing import Any, AsyncGenerator
from collections import defaultdict
from collections.abc import Callable

from app.domain.base import BaseEvent
from app.infrastructure.database.redis.conn import RedisCon

from redis.asyncio import Redis

import asyncio
import json
import logging

logger = logging.getLogger('chat_app')

class MessageBus:

    def __init__(self, redis_: Redis):
        self._redis: Redis = redis_
        self._pubsub = self._redis.pubsub()
        self._events: dict[str, type[BaseEvent]] = {}
        self._handlers: dict[type[BaseEvent], list[Callable]] = defaultdict(list)

    async def start_listen(self) -> None:
        while True:
            try:
                async for message in self._pubsub.listen():
                    if message['type'] == 'message':
                        data = json.loads(message['data'])
                        event_name = message['channel'].removeprefix('event:')
                        event_type = self._events[event_name]
                        event = event_type(**data)

                        for handler in self._handlers[event_type]:
                            await handler(event)
            except Exception:
                logger.exception("Redis pub/sub connection failed, retrying")
                await asyncio.sleep(3)
        
    async def publish_event(self, event: BaseEvent) -> None:
        event_type = type(event)
        channel = f"event:{event_type.__name__}"

        await self._redis.publish(channel, message=json.dumps(event.as_dict()))

    async def subscribe(self, event_type: type[BaseEvent], handler: Callable) -> None:
        event_name = event_type.__name__
        channel = f"event:{event_name}"
        self._events[event_name] = event_type
        self._handlers[event_type].append(handler)

        await self._pubsub.subscribe(channel)

message_bus = MessageBus(RedisCon.get_redis())