from app.domain.user import User
from app.domain.chat import Chat, ChatType
from app.domain.message import Message
from app.infrastructure.cache import MessagesCache

import pytest, pytest_asyncio

from collections.abc import Callable
from redis.asyncio import Redis, ConnectionPool

@pytest.fixture()
def user_maker() -> Callable[[str, str, str, int], User]:
    def _make(username: str, password: str, email: str, id_: int) -> User:
        user = User.create(username, email, password)
        user.id = id_
        return user

    return _make

@pytest.fixture()
def chat_maker() -> Callable[[str, set[User], ChatType], Chat]:
    def _make(chat_name: str, members: set[User], chat_type: ChatType) -> Chat:
        chat = Chat.create(chat_name, members, chat_type)
        return chat

    return _make

@pytest.fixture()
def default_direct_chat(chat_maker, user_maker) -> Chat:
    first_user = user_maker("first_user", "1Q2w3e", "maks@mail.ru", 1)
    second_user = user_maker("second_user", "1Q2w3e", "bob@mail.ru", 2)
    chat = chat_maker("default chat", {first_user, second_user}, ChatType.DIRECT)

    return chat


@pytest.fixture()
def direct_message_maker(user_maker, chat_maker) -> Callable[[str, int], Message]:
    def _make(text: str, message_id: int) -> Message:
        sender = user_maker("test_sender", "1Q2w3e", "test@mail.ru", 11)
        receiver = user_maker("test_receiver", "1Q2w3e", "test2@mail.ru", 12)
        chat = chat_maker("test_chat", {sender, receiver}, ChatType.DIRECT)
        message = Message.create(sender=sender, text=text, chat=chat)
        message.id = message_id
        return message

    return _make

@pytest_asyncio.fixture
async def redis_connection():
    pool = ConnectionPool.from_url(url="redis://localhost:6379/15", decode_responses=True)
    connection = Redis(connection_pool=pool)
    await connection.flushdb()
    yield connection
    await connection.aclose()

@pytest.fixture()
def message_cache(redis_connection):
    return MessagesCache(redis_connection)
