from app.infrastructure.database.redis.conn import RedisDep
from fastapi import Depends

from typing import Annotated

class TokenRepository:

    def __init__(self, redis_: RedisDep):
        self._redis = redis_

    async def add_refresh_token(self, refresh_token: str, username: str):
        self._redis.set(name=f"refresh_token:{refresh_token}", value=f"username:{username}", ex=86400)
        return {"status": "Successfully added"}

    async def get_username_by_refresh_token(self, refresh_token: str):
        username = self._redis.get(name=f"refresh_token:{refresh_token}")
        if not username:
            return None
        return username.decode()

    async def delete_refresh_token(self, refresh_token: str):
        return self._redis.delete(f"refresh_token:{refresh_token}")

async def get_token_repository(redis_: RedisDep):
    return TokenRepository(redis_)

TokenRepositoryDep = Annotated[TokenRepository, Depends(get_token_repository)]