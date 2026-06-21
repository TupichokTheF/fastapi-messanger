from app.infrastructure.cache import MessagesCache
from app.domain.message import Message
from app.domain.chat import Chat, ChatType
from app.domain.user import User

import pytest

from collections.abc import Callable


class TestMessageCache:

    async def test_cache_messages(self,
                                  message_cache,
                                  direct_message_maker: Callable[[str, int, int], Message]):
        message = direct_message_maker('Hello world!', 1, 1)
        async with message_cache as pipe:
            pipe.cache_message(message)

        messages = await message_cache.get_last_messages(message.chat)
        expected_data = {
            "message_id": str(message.id),
            "sender": message.sender.username,
            'created_at': str(int(message.chat.created_at.timestamp() * 1000)),
            'text': message.text
        }

        assert [expected_data] == messages

    async def test_message_cache_update(self,
                                        message_cache,
                                        direct_message_maker: Callable[[str, int, int], Message]):
        async with message_cache as pipe:
            for key in range(60):
                message = direct_message_maker('Hello world!', key, 1)
                pipe.cache_message(message)
        messages = await message_cache.get_last_messages(message.chat)

        assert len(messages) == 50
