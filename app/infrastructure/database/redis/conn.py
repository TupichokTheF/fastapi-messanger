from redis.asyncio import Redis, ConnectionPool

from app.core.settings import settings

class RedisConnection:

    def __init__(self):
        self._connection_pool = ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True, max_connections=10)

    def get_redis(self):
        return Redis(connection_pool=self._connection_pool)

    async def dispose_redis(self):
        await self._connection_pool.aclose()

RedisCon = RedisConnection()