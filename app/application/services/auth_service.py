from app.infrastructure.cache import TokenCache
from app.application.services.exceptions import WrongTokenError, NotFoundError, WrongPasswordError
from app.application.services.jwt_service import JWTService
from app.application.dtos import UserDTO
from app.domain.user import User, AbstractUserRepository


class AuthService:

    def __init__(self,
                 user_repo: AbstractUserRepository,
                 token_cache: TokenCache,
                 jwt_service: JWTService):
        self._user_repo = user_repo
        self._token_cache = token_cache
        self._jwt_service = jwt_service

    async def authenticate_user(self, username: str, password: str) -> UserDTO:
        user = await self._user_repo.get_user_by_username(username)
        if not user:
            raise NotFoundError("Incorrect username")
        if not user.verify_password(password):
            raise WrongPasswordError("Incorrect password")
        return UserDTO.from_entity(user)

    async def get_active_user(self, access_token: str, refresh_token: str) -> UserDTO:
        if await self._check_if_user_logout(refresh_token):
            raise WrongTokenError("Invalid token")
        user = await self._get_user_by_token(access_token)
        return UserDTO.from_entity(user)

    async def _check_if_user_logout(self, refresh_token: str) -> bool:
        return not await self._token_cache.get_username_by_refresh_token(refresh_token)

    async def _get_user_by_token(self, access_token: str) -> User:
        username = self._jwt_service.get_username_by_access_token(access_token)
        user = await self._user_repo.get_user_by_username(username)
        if user is None:
            raise NotFoundError("User not found by username")
        return user

