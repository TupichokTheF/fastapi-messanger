from redis.asyncio import Redis
from redis.client import Pipeline

from app.domain.chat import Chat, ChatType
from app.domain.message import Message
from app.domain.user import User

import asyncio

class ChatCachePipeline:

    def __init__(self, pipeline_: Pipeline):
        self._pipeline = pipeline_

    def update_user_chats(self, chat: Chat) -> None:
        chat_name = chat.name
        if chat.type == ChatType.DIRECT:
            first, second = chat.members
            chat_name = f"{first.user.username}_{second.user.username}"
        self._pipeline.hset(f"chat:{chat.id}:preview", mapping={"chat_name": chat_name, "chat_type": chat.type})

    def update_chat_score(self, user: User, chat: Chat) -> None:
        score = int(chat.created_at.timestamp() * 1000)
        self._pipeline.zadd(f"chats:{user.id}", {f"chat:{chat.id}": score})

    def update_chat_preview(self, chat: Chat, message: Message) -> None:
        preview_data = {
            "chat_id": chat.id,
            "chat_name": chat.name,
            "last_message": message.text,
            "last_message_spender": message.spender.username,
            "last_message_spend": message.created_at.timestamp()
        }
        self._pipeline.hset(f"chat:{chat.id}:preview", mapping=preview_data)


class ChatCache:

    def __init__(self, redis_: Redis):
        self._redis = redis_
        self._pipeline = self._redis.pipeline(transaction=False)

    async def get_chat_ids(self, user: User) -> list[int]:
        chats = await self._redis.zrevrange(f"chats:{user.id}", 0, -1)
        res = [int(chat.split(':')[-1]) for chat in chats]
        return res

    async def get_chats_previews(self, chat_ids: list[int]) -> list[dict]:
        for chat_id in chat_ids:
            self._pipeline.hgetall(f"chat:{chat_id}:preview")
        return await self._pipeline.execute()

    async def __aenter__(self):
        return ChatCachePipeline(self._pipeline)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            await self._pipeline.execute()
        else:
            await self._pipeline.reset()
        return False


async def main():
    redis = ChatCache(Redis(decode_responses=True))
    data = await redis.get_chats_previews([1])

    print(data)

if __name__ == "__main__":
    asyncio.run(main())