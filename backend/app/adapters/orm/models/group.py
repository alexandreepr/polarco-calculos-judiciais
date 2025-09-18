from typing import List, Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.adapters.orm.models.base import Base
from backend.app.adapters.orm.models.role import Role
from backend.app.adapters.orm.models.user import User

from backend.app.adapters.orm.models.association_tables import group_roles, user_groups
class Group(Base):
    __tablename__ = 'groups'

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    users: Mapped[List["User"]] = relationship(secondary=user_groups, back_populates="groups")
    roles: Mapped[List["Role"]] = relationship(secondary=group_roles, back_populates="groups")
