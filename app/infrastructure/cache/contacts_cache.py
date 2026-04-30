from redis import Redis

from app.domain.user import Contact, User

class ContactsCache:

    def __init__(self, redis_: Redis):
        self._redis = redis_

    async def add_contact(self, contact: Contact):
        score = int(contact.created_at.timestamp() * 1000)
        return self._redis.zadd(f"contacts:{contact.user.id}", {f"user:{contact.contact.id}": score})

    async def get_contacts_ids(self, user: User):
        raw_contacts = self._redis.zrevrange(f"contacts:{user.id}", 0, -1)
        user_contacts = [int(contact.decode().split(":")[-1]) for contact in raw_contacts]
        return user_contacts


if __name__ == "__main__":
    redis = Redis()
    data = redis.zrevrange(f"contacts:{2}", 0, -1, withscores=True)
    #a = data[0].decode().split(':')
    print(data)
