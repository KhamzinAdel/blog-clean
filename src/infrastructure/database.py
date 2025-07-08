from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import PostgresSettings


def new_session_maker(psql_settings: PostgresSettings) -> async_sessionmaker[AsyncSession]:
    database_uri = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
        user=psql_settings.POSTGRES_USER,
        password=psql_settings.POSTGRES_PASSWORD,
        host=psql_settings.POSTGRES_HOST,
        port=psql_settings.POSTGRES_PORT,
        db=psql_settings.POSTGRES_DB,
    )

    engine = create_async_engine(url=database_uri)
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
