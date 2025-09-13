
from .base import Base
from typing import List
from datetime import datetime
from sqlalchemy import String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .role import Role, user_roles
from .permission import Permission, user_permissions
from .group import Group, user_groups
from .audit_log import AuditLog

class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True) 
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    roles: Mapped[List["Role"]] = relationship(secondary=user_roles, back_populates="users")
    direct_permissions: Mapped[List["Permission"]] = relationship(secondary=user_permissions, back_populates="users")
    groups: Mapped[List["Group"]] = relationship(secondary=user_groups, back_populates="users")
    audit_logs: Mapped[List["AuditLog"]] = relationship(back_populates="user")