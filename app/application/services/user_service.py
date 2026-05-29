from app.domain.user import User, AbstractUserRepository


class UserService:

    def __init__(self, user_repo: AbstractUserRepository):
        self._user_repo = user_repo

    async def get_user_info(self, user: User) -> dict:
        user_info = user.to_dict()
        return user_info

