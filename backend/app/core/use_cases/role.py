from fastapi import HTTPException, status, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from backend.app.adapters.orm.models.role import Role
from backend.app.adapters.orm.models.user import User
from backend.app.adapters.orm.security.audit import create_audit_log
from backend.app.core.value_objects.role import RoleCreate

async def create_role_use_case(
    role: RoleCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    try:
        db_role = Role(**role.model_dump())
        db.add(db_role)
        await db.commit()
        await db.refresh(db_role)

        background_tasks.add_task(
            create_audit_log,
            db=db,
            user_id=current_user.id,
            action="create",
            resource_type="roles",
            resource_id=db_role.id,
            details=role.model_dump(),
            ip_address=request.client.host if request and request.client else None
        )

        return db_role
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role name already exists"
        )