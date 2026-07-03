from typing import Annotated

from fastapi import Depends

from app.infrastructure.cache import ChatCache, MessagesCache, TokenCache
from app.presentation.api.v1.dependencies.session_dep import RedisDep


def get_token_cache(redis: RedisDep):
    return TokenCache(redis)

def get_chat_cache(redis: RedisDep):
    return ChatCache(redis)

def get_message_cache(redis: RedisDep):
    return MessagesCache(redis)

ChatCacheDep = Annotated[ChatCache, Depends(get_chat_cache)]
TokenCacheDep = Annotated[TokenCache, Depends(get_token_cache)]
MessageCacheDep = Annotated[MessagesCache, Depends(get_message_cache)]

