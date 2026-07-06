from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

from app.domain.message import Message
from app.application.dtos import MessageDTO


class MessageCachePipe:

    def __init__(self, pipeline: Pipeline):
        self._pipe = pipeline

    def cache_message(self, message: Message) -> None:
        score = int(message.chat.created_at.timestamp() * 1000)
        message_data = {
            'message_id': message.id,
            'chat_id': message.chat.id,
            'sender_id': message.sender.id,
            'created_at': score,
            'text': message.text
        }
        self._pipe.hset(name=f'message:{message.id}', mapping=message_data)
        self._pipe.zadd(name=f'chat:{message.chat.id}:messages', mapping={f'message:{message.id}': score})
        self._pipe.zremrangebyrank(name=f'chat:{message.chat.id}:messages', min=0, max=-51)


class MessagesCache:

    def __init__(self, redis_: Redis):
        self._redis = redis_
        self._pipeline = self._redis.pipeline(transaction=False)

    async def get_last_messages_by_chat_id(self, chat_id: int) -> list[MessageDTO]:
        messages_keys = await self._redis.zrevrange(name=f'chat:{chat_id}:messages', start=0, end=-1)
        for message_key in messages_keys:
            self._pipeline.hgetall(name=message_key)
        messages_data = await self._pipeline.execute()

        return [self._convert_to_dto(message_data) for message_data in messages_data]

    @staticmethod
    def _convert_to_dto(data: dict) -> MessageDTO:
        return MessageDTO(message_id=data['message_id'],
                          chat_id=data['chat_id'],
                          sender_id=data['sender_id'],
                          created_at_timestamp_ms=data['created_at'],
                          text=data['text'])

    async def __aenter__(self) -> MessageCachePipe:
        return MessageCachePipe(self._pipeline)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            await self._pipeline.execute()
        else:
            await self._pipeline.reset()
        return False

