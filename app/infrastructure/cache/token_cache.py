from redis import Redis


class TokenCache:

    def __init__(self, redis_: Redis):
        self._redis = redis_

    async def add_refresh_token(self, refresh_token: str, username: str):
        self._redis.set(name=f"refresh_token:{refresh_token}", value=f"username:{username}", ex=86400)
        return {"status": "Successfully added"}

    async def get_username_by_refresh_token(self, refresh_token: str):
        username = self._redis.get(name=f"refresh_token:{refresh_token}")
        if not username:
            return None
        return username.decode().split(':')[-1]

    async def delete_refresh_token(self, refresh_token: str):
        return self._redis.delete(f"refresh_token:{refresh_token}")
