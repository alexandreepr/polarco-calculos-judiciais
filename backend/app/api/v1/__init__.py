from fastapi import APIRouter

from .processos import router as processos_router

router = APIRouter(prefix="/v1")
router.include_router(processos_router)