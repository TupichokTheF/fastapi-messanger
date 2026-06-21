from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

from app.domain.message import Message
from app.domain.chat import Chat

class MessageCachePipe:

    def __init__(self, pipeline: Pipeline):
        self._pipe = pipeline

    def cache_message(self, message: Message):
        score = int(message.chat.created_at.timestamp() * 1000)
        message_data = {
            "message_id": message.id,
            "sender": message.sender.username,
            'created_at': score,
            'text': message.text
        }
        self._pipe.hset(name=f'message:{message.id}', mapping=message_data)
        self._pipe.zadd(name=f'chat:{message.chat.id}:messages', mapping={f'message:{message.id}': score})


class MessagesCache:

    def __init__(self, redis_: Redis):
        self._redis = redis_
        self._pipeline = self._redis.pipeline(transaction=False)

    async def get_last_messages(self, chat: Chat):
        messages_keys = await self._redis.zrevrange(name=f'chat:{chat.id}:messages', start=0, end=-1)
        for message_key in messages_keys:
            self._pipeline.hgetall(name=message_key)
        messages_data = await self._pipeline.execute()

        return messages_data

    async def __aenter__(self) -> MessageCachePipe:
        return MessageCachePipe(self._pipeline)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            await self._pipeline.execute()
        else:
            await self._pipeline.reset()
        return False

