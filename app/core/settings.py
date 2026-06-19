from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

from datetime import timedelta
from pathlib import Path

class Settings(BaseSettings):
    BASE_PATH: str = str(Path(__file__).resolve().parents[1])
    LOGGING_CONFIG: str = f"{BASE_PATH}/core/logging/config.json"

    model_config = SettingsConfigDict(
        env_file=f'{BASE_PATH}/../.env.local',
        extra='ignore'
    )

    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DATABASE: str = ""

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_DATABASE
        )

    REDIS_HOST: str = ""
    REDIS_PORT: int = 6379

    ALGORITHM_OF_CIFER: str = "HS256"
    JWT_SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=1)

settings = Settings()