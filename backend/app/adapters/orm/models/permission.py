from typing import Any, Dict, List, Optional
from sqlalchemy import String, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .association_tables import role_permissions, user_permissions


class Permission(Base):
    __tablename__ = 'permissions'

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    resource: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(String(50))
    conditions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    roles: Mapped[List["Role"]] = relationship(secondary=role_permissions, back_populates="permissions")
    users: Mapped[List["User"]] = relationship(secondary=user_permissions, back_populates="direct_permissions")

from .role import Role
from .user import User