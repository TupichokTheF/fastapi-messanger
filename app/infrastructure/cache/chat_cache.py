from redis.asyncio import Redis

from app.domain.chat import Chat, ChatType
from app.domain.message import Message
from app.domain.user import User

import asyncio

class ChatCache:

    def __init__(self, redis_: Redis):
        self._redis = redis_

    async def update_user_chats(self, chat: Chat) -> bool:
        chat_name = chat.name
        if chat.type == ChatType.DIRECT:
            first, second = chat.members
            chat_name = f"{first.user.username}_{second.user.username}"
        await self._redis.hset(f"chat:{chat.id}:preview", mapping={"chat_name": chat_name, "chat_type": chat.type})
        return True

    async def update_chat_score(self, user: User, chat: Chat):
        score = int(chat.created_at.timestamp() * 1000)
        return await self._redis.zadd(f"chats:{user.id}", {f"chat:{chat.id}": score})

    async def get_chat_ids(self, user: User) -> list[int]:
        chats = await self._redis.zrevrange(f"chats:{user.id}", 0, -1)
        res = [int(chat.split(':')[-1]) for chat in chats]
        return res

    async def get_chats_previews(self, chat_ids: list[int]) -> list[dict]:
        res = []
        for chat_id in chat_ids:
            chat_preview = await self._redis.hgetall(f"chat:{chat_id}:preview")
            res.append(chat_preview)
        return res

    async def update_chat_preview(self, chat: Chat, message: Message) -> int:
        preview_data = {
            "chat_name": chat.name,
            "last_message": message.text,
            "last_message_spender": message.spender.username,
            "last_message_spend": message.created_at.timestamp()
        }
        return await self._redis.hset(f"chat:{chat.id}:preview", mapping=preview_data)



async def main():
    redis = ChatCache(Redis())
    data = await redis.get_chats_previews([1])

    print(data)

if __name__ == "__main__":
    asyncio.run(main())