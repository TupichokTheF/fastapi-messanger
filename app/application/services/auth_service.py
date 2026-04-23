from app.infrastructure.adapters.repositories import UserRepository, TokenRepository
from app.application.services.exceptions import WrongTokenError, NotFoundError, WrongPasswordError
from app.application.services.jwt_service import JWTService
from app.domain.user import User


class AuthService:

    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository, jwt_service: JWTService):
        self._user_repo = user_repo
        self._token_repo = token_repo
        self._jwt_service = jwt_service

    async def authenticate_user(self, username: str, password: str):
        user = await self._user_repo.get_user_by_username(username)
        if not user:
            raise NotFoundError("Incorrect username")
        if not user.verify_password(password):
            raise WrongPasswordError("Incorrect password")
        return user

    async def get_active_user(self, access_token: str, refresh_token: str):
        if await self.check_if_user_logout(refresh_token):
            return None
        return await self.get_user_by_token(access_token)

    async def check_if_user_logout(self, refresh_token: str) -> bool:
        if not await self._token_repo.get_username_by_refresh_token(refresh_token):
            return True
        return False

    async def get_user_by_token(self, access_token: str) -> User:
        try:
            username = self._jwt_service.get_username_by_access_token(access_token)
            if username is None:
                raise WrongTokenError("Invalid username")
        except WrongTokenError as exc:
            raise exc
        user = await self._user_repo.get_user_by_username(username)
        if user is None:
            raise NotFoundError("User not found by username")
        return user

