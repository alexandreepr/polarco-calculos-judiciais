
from sqlalchemy import ForeignKey, String
import uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from .base import Base
from .association_tables import company_user

class Company(Base):
    __tablename__ = 'company'

    name: Mapped[str] = mapped_column(String, nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    owner: Mapped['User'] = relationship('User', foreign_keys=[owner_id])
    created_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_by: Mapped['User'] = relationship('User', foreign_keys=[created_by_id])
    deleted_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey('users.id'), nullable=True)
    deleted_by: Mapped[Optional['User']] = relationship('User', foreign_keys=[deleted_by_id])
    members: Mapped[List['User']] = relationship(
        'User',
        secondary=company_user,
        back_populates='companies',
        lazy='selectin'
    )

from .user import User