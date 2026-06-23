from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession


from app.core.settings import settings
from app.infrastructure.database.postgresql.mappers import init_tables, metadata


class Database:

    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._session: async_sessionmaker[AsyncSession] | None = None

    async def get_session(self):
        if self._session is not None:
            async with self._session() as session:
                yield session

    async def init_database(self):
        init_tables()
        self._engine = create_async_engine(str(settings.DATABASE_URL))
        self._session = async_sessionmaker(self._engine, expire_on_commit=False)
        async with self._engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    async def dispose_database(self):
        await self._engine.dispose()

database = Database()