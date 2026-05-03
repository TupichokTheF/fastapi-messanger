from app.infrastructure.adapters.repositories import UserRepository
from app.domain.user import User


class UserService:

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def create_user(self, user_data: User):
        return await self._user_repo.create_user(user_data)
