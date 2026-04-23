import redis

from app.core.settings import settings

def get_redis():
    connection = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return connection