from app.application.dtos.user_dto import UserSignUpDTO
from app.domain.user import AbstractUserRepository


class UserService:

    def __init__(self, user_repo: AbstractUserRepository):
        self._user_repo = user_repo

    async def create_user(self, user_dto: UserSignUpDTO):
        user = user_dto.to_entity()
        user_id = await self._user_repo.create_user(user)

        return user_id
