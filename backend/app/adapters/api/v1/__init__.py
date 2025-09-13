from fastapi import APIRouter

from user import user_router
from auth import auth_router
from company import company_router

router = APIRouter(prefix="/v1")
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(company_router)