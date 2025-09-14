from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from models.audit_log import AuditLog

async def create_audit_log(
    db: AsyncSession,
    user_id: Optional[int],
    action: str,
    resource_type: str,
    resource_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None
) -> AuditLog:
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address
    )
    db.add(audit_log)
    await db.commit()
    await db.refresh(audit_log)
    return audit_log