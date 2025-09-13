
from typing import List
from datetime import datetime
from sqlalchemy import String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.adapters.orm.models.company import Company
from base import Base
from role import Role
from permission import Permission
from group import Group
from audit_log import AuditLog
from association_tables import user_groups, user_roles, user_permissions, company_user

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
    companies: Mapped[List["Company"]] = relationship(secondary=company_user, back_populates="members")