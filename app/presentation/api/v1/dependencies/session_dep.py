from app.infrastructure.database.postgresql.db import database
from app.infrastructure.database.redis.conn import get_redis

from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
import redis

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
RedisDep = Annotated[redis.Redis, Depends(get_redis)]