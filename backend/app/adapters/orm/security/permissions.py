from datetime import datetime
from typing import Any, Dict, Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.adapters.orm.models.user import User
from app.adapters.orm.security.auth import get_current_active_user
from app.adapters.orm.database import get_async_db


# ABAC Permission verification
async def has_permission(
    user: User,
    resource: str,
    action: str,
    # resource_id: Optional[int] = None,
    context: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Check if user has permission to perform an action on a resource.
    Implements Attribute-Based Access Control (ABAC) by considering:
    - Direct user permissions
    - Role-based permissions
    - Group-based permissions
    - Contextual conditions
    """
    context = context or {}

    # Helper function to check conditions
    def evaluate_conditions(conditions: Optional[Dict[str, Any]], context: Dict[str, Any]) -> bool:
        if not conditions:
            return True

        # Example condition: {"time_between": ["09:00", "17:00"]}
        for condition_key, condition_value in conditions.items():
            if condition_key == "time_between":
                current_time = context.get("current_time", datetime.now().time())
                start_time = datetime.strptime(condition_value[0], "%H:%M").time()
                end_time = datetime.strptime(condition_value[1], "%H:%M").time()
                if not (start_time <= current_time <= end_time):
                    return False
            elif condition_key == "ip_range":
                ip = context.get("ip_address")
                if not ip or ip not in condition_value:
                    return False
            # Add more condition types as needed

        return True

    # Check direct user permissions
    for permission in user.direct_permissions:
        if (permission.resource == resource and 
            permission.action == action and 
            evaluate_conditions(permission.conditions, context)):
            return True

    # Check role-based permissions
    for role in user.roles:
        for permission in role.permissions:
            if (permission.resource == resource and 
                permission.action == action and 
                evaluate_conditions(permission.conditions, context)):
                return True

    # Check group-based permissions (through roles)
    for group in user.groups:
        for role in group.roles:
            for permission in role.permissions:
                if (permission.resource == resource and 
                    permission.action == action and 
                    evaluate_conditions(permission.conditions, context)):
                    return True

    return False

# Permission dependency for FastAPI routes
def require_permission(resource: str, action: str):
    async def permission_dependency(
        request: Request,
        db=Depends(get_async_db),
        current_user: User = Depends(get_current_active_user)
    ):
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.direct_permissions),
                selectinload(User.roles),
                selectinload(User.groups),
            )
            .where(User.id == current_user.id)
        )
        user_with_permissions = result.scalars().first()

        context: Dict[str, Any] = {
            "current_time": datetime.now().time(),
            "ip_address": request.client.host if request and request.client else None
        }

        if not await has_permission(user_with_permissions, resource, action, context=context):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {action} on {resource}"
            )
        return user_with_permissions
    return permission_dependency
