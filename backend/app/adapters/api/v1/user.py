from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.adapters.orm.models.user import User
from app.core.use_cases.user import (
    create_user_use_case,
    get_users_use_case,
    get_user_use_case,
    update_user_use_case,
    delete_user_use_case
)
from app.adapters.orm.security.permissions import require_permission
from app.adapters.orm.database import get_async_db
from app.core.value_objects import UserCreate, UserResponse, UserUpdate

user_router = APIRouter(prefix="/users", tags=["User Management"])

@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    # current_user: User = Depends(require_permission("users", "create"))
):
    db_user = await create_user_use_case(db, user, background_tasks, request)
    return db_user

@user_router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("users", "list"))
):
    users = await get_users_use_case(db, skip, limit)
    return users

@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("users", "view"))
):
    db_user = await get_user_use_case(user_id, db)
    return db_user

@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("users", "update"))
):
    db_user = await update_user_use_case(user_id, user_update, background_tasks, current_user, db, request)
    return db_user

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("users", "delete"))
):
    response = await delete_user_use_case(user_id, background_tasks, db, current_user, request)
    return response