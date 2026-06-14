from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from app.core.settings import settings
from app.infrastructure.database.postgresql.mappers import init_tables, metadata


class Database:

    def __init__(self):
        self._engine = create_async_engine(str(settings.DATABASE_URL))
        self._session = async_sessionmaker(self._engine, expire_on_commit=False)

    async def get_session(self):
        async with self._session() as session:
            yield session

    async def init_database(self):
        init_tables()
        async with self._engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    async def dispose_database(self):
        await self._engine.dispose()

database = Database()