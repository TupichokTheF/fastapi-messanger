from redis import Redis



class MessagesCache:

    def __init__(self, redis_: Redis):
        self._redis = redis_
