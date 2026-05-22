from app.infrastructure.adapters.repositories import UserRepository
from app.domain.user import User


class UserService:

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def get_user_info(self, user: User) -> dict:
        user_info = user.to_dict()
        return user_info

