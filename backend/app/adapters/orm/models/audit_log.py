import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import ForeignKey, String, JSON, Integer, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    action: Mapped[str] = mapped_column(String(50))
    resource_type: Mapped[str] = mapped_column(String(50))
    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    user: Mapped[Optional["User"]] = relationship(back_populates="audit_logs")

from .user import User