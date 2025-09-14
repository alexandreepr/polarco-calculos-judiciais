from fastapi import Cookie, Depends, HTTPException, Request, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.value_objects.token import TokenResponse
from backend.app.adapters.orm.database import get_async_db
from app.core.use_cases.auth import login_for_access_token_use_case, refresh_access_token_use_case

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    request: Request,
    background_tasks: BackgroundTasks,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    
    token = await login_for_access_token_use_case(db, form_data, background_tasks, request)

    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60*60*24*7
    )

    return TokenResponse(
        access_token=token.access_token,
        token_type=token.token_type
    )

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db),
    refresh_token: str = Cookie(None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    
    token = await refresh_access_token_use_case(refresh_token, db, background_tasks, request)

    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60*60*24*7
    )
    return TokenResponse(
        access_token=token.access_token,
        token_type=token.token_type
    )