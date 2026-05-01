from redis import Redis

from app.domain.message import MessageReceiver

class MessagesCache:

    def __init__(self, redis_: Redis):
        self._redis = redis_

    async def update_last_message(self, message_receiver: MessageReceiver):
        message = message_receiver.message
        receiver = message_receiver.receiver
        self._redis.hset(f"last_messages:{receiver.id}", f"user:{message.spender.id}", message.text)
        self._redis.hset(f"last_messages:{message.spender.id}", f"user:{receiver.id}", message.text)
        return True