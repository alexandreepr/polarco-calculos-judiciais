from fastapi import HTTPException, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.core.value_objects.token import Token
from backend.app.adapters.orm.security.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from backend.app.adapters.orm.security.audit import create_audit_log

async def login_for_access_token_use_case(
    db: AsyncSession,
    form_data: OAuth2PasswordRequestForm,
    background_tasks: BackgroundTasks,
    request: Request
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    background_tasks.add_task(
        create_audit_log,
        db=db,
        user_id=user.id,
        action="login",
        resource_type="auth",
        details={"success": True},
        ip_address=request.client.host if request and request.client else None
    )

    return Token(access_token=access_token, token_type="bearer")