from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.adapters.orm.models.base import Base
from app.adapters.orm.database import async_engine
from .infrastructure.config import settings
from .infrastructure.logger import logger
from .adapters.api import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created (if not exist)")
    yield

app = FastAPI(lifespan=lifespan)

origins = settings.get("ALLOWED_ORIGINS")

logger.info('API is starting up')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
