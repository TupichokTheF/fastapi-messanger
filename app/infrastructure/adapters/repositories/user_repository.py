from app.domain.user import User, AbstractUserRepository
from app.domain.user.value_objects import UserUsername

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(AbstractUserRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, user: User) -> int:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user.id

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).filter_by(id=user_id)
        res = await self._session.execute(query)

        return res.scalars().first()

    async def get_user_by_username(self, raw_username: str) -> User:
        username = UserUsername(raw_username)
        query = select(User).filter_by(_username=username)
        res = await self._session.execute(query)
        return res.scalars().first()
