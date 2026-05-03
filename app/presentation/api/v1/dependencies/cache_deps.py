from app.infrastructure.cache import TokenCache
from app.presentation.api.v1.dependencies import RedisDep

from fastapi import Depends
from typing import Annotated


def get_token_cache(redis: RedisDep):
    return TokenCache(redis)


TokenCacheDep = Annotated[TokenCache, Depends(get_token_cache)]

