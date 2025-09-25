from fastapi import BackgroundTasks, HTTPException, Request, Response, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.adapters.orm.models.permission import Permission
from app.adapters.orm.models.role import Role
from app.adapters.orm.models.user import User
from app.adapters.orm.security.audit import create_audit_log
from app.core.value_objects.permission import PermissionCreate

async def create_permission_use_case(
    permission: PermissionCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    try:
        db_permission = Permission(**permission.model_dump())
        db.add(db_permission)
        await db.commit()
        await db.refresh(db_permission)

        # Log permission creation in background
        background_tasks.add_task(
            create_audit_log,
            db=db,
            user_id=current_user.id,
            action="create",
            resource_type="permissions",
            resource_id=db_permission.id,
            details=permission.model_dump(),
            ip_address=request.client.host if request and request.client else None
        )

        return db_permission
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission with this resource and action already exists"
        )

async def get_permissions_use_case(
    db: AsyncSession,
    skip: int,
    limit: int
):
    stmt = select(Permission).offset(skip).limit(limit)
    result = await db.execute(stmt)
    permissions = result.scalars().all()
    return permissions

async def get_permission_use_case(
    permission_id: int,
    db: AsyncSession
):
    stmt = select(Permission).where(Permission.id == permission_id)
    result = await db.execute(stmt)
    db_permission = result.scalars().first()

    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

async def update_permission_use_case(
    permission_id: int,
    permission_update: PermissionCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    stmt = select(Permission).where(Permission.id == permission_id)
    result = await db.execute(stmt)
    db_permission = result.scalars().first()

    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    update_data = permission_update.model_dump()

    try:
        stmt = (
            update(Permission)
            .where(Permission.id == permission_id)
            .values(**update_data)
        )
        await db.execute(stmt)
        await db.commit()

        # Refresh permission data
        stmt = select(Permission).where(Permission.id == permission_id)
        result = await db.execute(stmt)
        db_permission = result.scalars().first()

        # Log permission update in background
        background_tasks.add_task(
            create_audit_log,
            db=db,
            user_id=current_user.id,
            action="update",
            resource_type="permissions",
            resource_id=permission_id,
            details=update_data,
            ip_address=request.client.host if request and request.client else None
        )

        return db_permission
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission with this resource and action already exists"
        )
    
## TODO: implement soft delete, review all delete from all resources
async def delete_permission_use_case(
    permission_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    stmt = select(Permission).where(Permission.id == permission_id)
    result = await db.execute(stmt)
    db_permission = result.scalars().first()

    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    # Store permission details for audit log
    permission_details = {
        "name": db_permission.name,
        "resource": db_permission.resource,
        "action": db_permission.action
    }

    stmt = delete(Permission).where(Permission.id == permission_id)
    await db.execute(stmt)
    await db.commit()

    # Log permission deletion in background
    background_tasks.add_task(
        create_audit_log,
        db=db,
        user_id=current_user.id,
        action="delete",
        resource_type="permissions",
        resource_id=permission_id,
        details=permission_details,
        ip_address=request.client.host if request and request.client else None
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

async def assign_permission_to_role_use_case(
    permission_id: int,
    role_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
        # Check if permission exists
    permission_stmt = select(Permission).where(Permission.id == permission_id)
    permission_result = await db.execute(permission_stmt)
    permission = permission_result.scalars().first()

    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    # Check if role exists
    role_stmt = select(Role).where(Role.id == role_id)
    role_result = await db.execute(role_stmt)
    role = role_result.scalars().first()

    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    # Add permission to role if not already assigned
    if permission not in role.permissions:
        role.permissions.append(permission)
        await db.commit()

        # Log assignment in background
        background_tasks.add_task(
            create_audit_log,
            db=db,
            user_id=current_user.id,
            action="assign",
            resource_type="permissions",
            resource_id=permission_id,
            details={"role_id": role_id, "permission_id": permission_id},
            ip_address=request.client.host if request and request.client else None
        )

    ## TODO: return permission updated
    return {"message": f"Permission '{permission.name}' assigned to role '{role.name}'"}
