from app.core.settings import settings
from app.infrastructure.cache import TokenCache
from app.application.services.exceptions import NotFoundError, WrongTokenError

from datetime import timedelta, timezone, datetime
import jwt
from jwt.exceptions import InvalidTokenError


class JWTService:

    def __init__(self, token_cache: TokenCache):
        self._token_cache = token_cache

    async def generate_refresh_token(self, data: dict):
        encoded_jwt = await self.generate_token(data, settings.REFRESH_TOKEN_EXPIRES)
        await self._token_cache.add_refresh_token(encoded_jwt, data["sub"])
        return encoded_jwt

    async def generate_token(self, data: dict, expires_delta: timedelta | None = settings.ACCESS_TOKEN_EXPIRES):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM_OF_CIFER)
        return encoded_jwt

    async def refresh_access_token(self, refresh_token: str):
        username = await self._token_cache.get_username_by_refresh_token(refresh_token)
        if not username:
            raise NotFoundError("Incorrect refresh_token")
        access_token = await self.generate_token({"sub": username})
        return access_token

    def get_username_by_access_token(self, access_token: str):
        try:
            payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM_OF_CIFER])
            username = payload.get("sub")
            return username
        except InvalidTokenError:
            raise WrongTokenError("Invalid access token")