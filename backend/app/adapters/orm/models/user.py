
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .association_tables import user_groups, user_roles, user_permissions, company_user

class User(Base):

    __tablename__ = 'users'

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    roles: Mapped[List["Role"]] = relationship(secondary=user_roles, back_populates="users")
    direct_permissions: Mapped[List["Permission"]] = relationship(secondary=user_permissions, back_populates="users")
    groups: Mapped[List["Group"]] = relationship(secondary=user_groups, back_populates="users")
    audit_logs: Mapped[List["AuditLog"]] = relationship(back_populates="user")
    companies: Mapped[List["Company"]] = relationship(secondary=company_user, back_populates="members")
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

from .company import Company
from .role import Role
from .permission import Permission
from .audit_log import AuditLog
from .group import Group