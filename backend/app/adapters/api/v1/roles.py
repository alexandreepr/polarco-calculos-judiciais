from fastapi import Depends, status, Request, BackgroundTasks
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.orm.database import get_async_db
from app.adapters.orm.models.user import User
from app.adapters.orm.security.permissions import require_permission
from app.core.value_objects.role import RoleCreate, RoleResponse
from app.core.use_cases.role import create_role_use_case

role_router = APIRouter(prefix="/roles", tags=["Role Management"])

@role_router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role: RoleCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_permission("roles", "create"))
):
    return await create_role_use_case(
        role=role,
        background_tasks=background_tasks,
        request=request,
        db=db,
        current_user=current_user
    )