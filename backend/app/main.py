from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logger import logger
from .api import router as api_router

app = FastAPI()

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
