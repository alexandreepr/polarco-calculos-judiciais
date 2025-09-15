from fastapi import HTTPException, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.value_objects.token import Token
from backend.app.adapters.orm.models.refresh_token import RefreshToken
from backend.app.adapters.orm.security.auth import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, create_refresh_token
from backend.app.adapters.orm.security.audit import create_audit_log

async def login_for_access_token_use_case(
    db: AsyncSession,
    form_data: OAuth2PasswordRequestForm,
    background_tasks: BackgroundTasks,
    request: Request,
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

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=7)
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

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

async def refresh_access_token_use_case(
    refresh_token: str,
    db: AsyncSession,
    background_tasks: BackgroundTasks,
    request: Request,
) -> Token:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # TODO: check token revocation/blacklist here
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user_id},
        expires_delta=timedelta(days=7)
    )

    if background_tasks and request:
        background_tasks.add_task(
            create_audit_log,
            db=db,
            user_id=user_id,
            action="refresh_token",
            resource_type="auth",
            details={"success": True},
            ip_address=request.client.host if request and request.client else None
        )
        
    return Token(access_token=access_token, refresh_token=new_refresh_token, token_type="bearer")

async def store_refresh_token(db: AsyncSession, user_id: int, token: str, expires_in_days: int = 7):
    expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
    db_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    
    return db_token

async def revoke_refresh_token(db: AsyncSession, token: str):
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
    db_token = result.scalars().first()
    if db_token:
        db_token.revoked = True
        await db.commit()

async def is_refresh_token_valid(db: AsyncSession, token: str, user_id: int):
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        )
    )

    return result.scalars().first() is not None