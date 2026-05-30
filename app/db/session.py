from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import get_settings
from app.db.base import Base

engine: AsyncEngine | None = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global engine
    if engine is None:
        engine = create_async_engine(
            get_settings().async_database_url,
            echo=False,
            future=True,
        )
    return engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    global AsyncSessionLocal
    if AsyncSessionLocal is None:
        AsyncSessionLocal = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return AsyncSessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_sessionmaker()() as session:
        yield session


async def ensure_database_exists() -> None:
    settings = get_settings()
    maintenance_engine = create_async_engine(
        settings.async_maintenance_database_url,
        isolation_level="AUTOCOMMIT",
    )

    try:
        async with maintenance_engine.connect() as connection:
            result = await connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
                {"database_name": settings.postgres_db},
            )
            if result.scalar_one_or_none() is None:
                database_name = settings.postgres_db.replace('"', '""')
                await connection.execute(text(f'CREATE DATABASE "{database_name}"'))
    finally:
        await maintenance_engine.dispose()


async def create_database_schema() -> None:
    await ensure_database_exists()
    async with get_engine().begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
