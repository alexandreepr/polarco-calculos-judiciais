from typing import List, Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .association_tables import user_groups, group_roles


class Group(Base):
    __tablename__ = 'groups'

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    users: Mapped[List["User"]] = relationship(secondary=user_groups, back_populates="groups")
    roles: Mapped[List["Role"]] = relationship(secondary=group_roles, back_populates="groups")

from .role import Role
from .user import User