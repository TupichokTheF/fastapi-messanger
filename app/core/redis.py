import redis

from typing import Annotated

from fastapi import Depends

from app.core.settings import settings

def get_redis():
    connection = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return connection

RedisDep = Annotated[redis.Redis, Depends(get_redis)]