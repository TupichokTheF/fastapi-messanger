from app.infrastructure.cache import TokenCache, ContactsCache, MessagesCache
from app.presentation.api.v1.dependencies import RedisDep

from fastapi import Depends
from typing import Annotated


def get_token_cache(redis: RedisDep):
    return TokenCache(redis)

def get_contacts_cache(redis: RedisDep):
    return ContactsCache(redis)

def get_messages_cache(redis: RedisDep):
    return MessagesCache(redis)

TokenCacheDep = Annotated[TokenCache, Depends(get_token_cache)]
ContactsCacheDep = Annotated[ContactsCache, Depends(get_contacts_cache)]
MessagesCacheDep = Annotated[MessagesCache, Depends(get_messages_cache)]
