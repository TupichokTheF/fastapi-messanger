from app.infrastructure.cache import TokenCache, ChatCache, MessagesCache
from app.presentation.api.v1.dependencies import RedisDep

from fastapi import Depends
from typing import Annotated


def get_token_cache(redis: RedisDep):
    return TokenCache(redis)

def get_chat_cache(redis: RedisDep):
    return ChatCache(redis)

def get_message_cache(redis: RedisDep):
    return MessagesCache(redis)

ChatCacheDep = Annotated[ChatCache, Depends(get_chat_cache)]
TokenCacheDep = Annotated[TokenCache, Depends(get_token_cache)]
MessageCacheDep = Annotated[MessagesCache, Depends(get_message_cache)]

