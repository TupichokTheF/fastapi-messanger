from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.postgresql.db import database
from app.infrastructure.database.redis.conn import RedisCon

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
RedisDep = Annotated[Redis, Depends(RedisCon.get_redis)]
