
from sqlalchemy import ForeignKey, String
import uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from backend.app.adapters.orm.models.base import Base
from backend.app.adapters.orm.models.association_tables import company_user
from backend.app.adapters.orm.models.user import User

class Company(Base):
    __tablename__ = 'company'

    name: Mapped[str] = mapped_column(String, nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    owner: Mapped['User'] = relationship('User', foreign_keys=[owner_id])
    created_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_by: Mapped['User'] = relationship('User', foreign_keys=[created_by_id])
    deleted_by_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    deleted_by: Mapped['User | None'] = relationship('User', foreign_keys=[deleted_by_id])
    members: Mapped[List['User']] = relationship(
        'User',
        secondary=company_user,
        back_populates='companies',
        lazy='selectin'
    )