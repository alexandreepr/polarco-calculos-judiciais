import uuid
from fastapi import BackgroundTasks, HTTPException, Request, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from typing import Optional

from ...adapters.orm.models.user import User
from ...adapters.orm.security.auth import get_password_hash
from ...adapters.orm.security import create_audit_log
from ..value_objects import UserUpdate
from ..value_objects import UserCreate

async def create_user_use_case(db: AsyncSession, user: UserCreate, background_tasks: BackgroundTasks, request: Request) -> User:
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            id=uuid.uuid4(),
            username=user.username,
            email=user.email,
            password_hash=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        # Log user creation in background
        background_tasks.add_task(
            create_audit_log,
            db=db,
            action="create",
            user_id=db_user.id,
            resource_type="users",
            resource_id=db_user.id,
            details={"username": user.username, "email": user.email},
            ip_address=request.client.host if request and request.client else None
        )

        return db_user
    except IntegrityError as e:
        print("IntegrityError:", e)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

async def get_users_use_case(db: AsyncSession, skip: int, limit: int):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

async def get_user_use_case(user_id: int, db: AsyncSession):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


async def update_user_use_case(
    user_id: int,
    user_update: UserUpdate,
    background_tasks: BackgroundTasks,
    current_user: User,
    db: AsyncSession,
    request: Optional[Request] = None,
):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)

    try:
        if update_data:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(**update_data)
            )
            await db.execute(stmt)
            await db.commit()

        # Refresh user data
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        db_user = result.scalars().first()

        # Log user update in background
        background_tasks.add_task(
            create_audit_log,
            db=db,
            user_id=current_user.id,
            action="update",
            resource_type="users",
            resource_id=user_id,
            details=update_data,
            ip_address=request.client.host if request and request.client else None
        )

        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

async def delete_user_use_case(
    user_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession,
    current_user: User,
    request: Optional[Request] = None,
):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Store username for audit log
    username = db_user.username

    stmt = delete(User).where(User.id == user_id)
    await db.execute(stmt)
    await db.commit()

    # Log user deletion in background
    background_tasks.add_task(
        create_audit_log,
        db=db,
        user_id=current_user.id,
        action="delete",
        resource_type="users",
        resource_id=user_id,
        details={"username": username},
        ip_address=request.client.host if request and request.client else None
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)