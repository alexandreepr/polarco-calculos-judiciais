

from typing import List, Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from group import Group
from permission import Permission
from user import User
from base import Base
import uuid
from association_tables import role_permissions, user_roles, group_roles

class Role(Base):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    users: Mapped[List["User"]] = relationship(secondary=user_roles, back_populates="roles")
    permissions: Mapped[List["Permission"]] = relationship(secondary=role_permissions, back_populates="roles")
    groups: Mapped[List["Group"]] = relationship(secondary=group_roles, back_populates="roles")