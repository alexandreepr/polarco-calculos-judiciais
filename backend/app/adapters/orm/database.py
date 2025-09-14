import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

# For async database operations
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "postgresql+asyncpg://polarco:polarco@postgres:5432/polarco")

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
)

SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL", "postgresql://polarco:polarco@postgres:5432/polarco")

sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=True,
    future=True,
)

SyncSessionLocal = sessionmaker(
    sync_engine, 
    class_=Session, 
    expire_on_commit=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session