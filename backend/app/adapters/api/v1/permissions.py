from fastapi import Depends, status, Request, BackgroundTasks
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.adapters.orm.database import get_async_db
from app.adapters.orm.models.user import User
from app.adapters.orm.security.permissions import require_permission
from app.core.value_objects.permission import PermissionCreate, PermissionResponse
from app.core.use_cases.permission import (
    create_permission_use_case,
    get_permissions_use_case,
    get_permission_use_case,
    update_permission_use_case,
    delete_permission_use_case,
    assign_permission_to_role_use_case
)


permission_router = APIRouter(prefix="/permissions", tags=["Permission Management"])

@permission_router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission: PermissionCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("permissions", "create"))
):
    return await create_permission_use_case(
        permission=permission,
        background_tasks=background_tasks,
        request=request,
        db=db,
        current_user=current_user
    )

@permission_router.get("/", response_model=List[PermissionResponse])
async def get_permissions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("permissions", "list"))
):
    return await get_permissions_use_case(db=db, skip=skip, limit=limit)

@permission_router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("permissions", "read"))
):
    return await get_permission_use_case(permission_id=permission_id, db=db)

@permission_router.put("/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_update: PermissionCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("permissions", "update"))
):
    return await update_permission_use_case(
        permission_id=permission_id,
        permission_update=permission_update,
        background_tasks=background_tasks,
        request=request,
        db=db,
        current_user=current_user
    )

@permission_router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    permission_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("permissions", "delete"))
):
    return await delete_permission_use_case(
        permission_id=permission_id,
        background_tasks=background_tasks,
        request=request,
        db=db,
        current_user=current_user
    )

@permission_router.post("/{permission_id}/assign-to-role/{role_id}", status_code=status.HTTP_200_OK)
async def assign_permission_to_role(
    permission_id: int,
    role_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("permissions", "assign"))
):
    return await assign_permission_to_role_use_case(
        permission_id=permission_id,
        role_id=role_id,
        background_tasks=background_tasks,
        request=request,
        db=db,
        current_user=current_user
    )
