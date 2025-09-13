from fastapi import Depends, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.value_objects.token import Token
from backend.app.adapters.orm.database import get_async_db
from app.core.use_cases.auth import login_for_access_token_use_case

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    background_tasks: BackgroundTasks,
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    return await login_for_access_token_use_case(
        db=db,
        form_data=form_data,
        background_tasks=background_tasks,
        request=request
    )