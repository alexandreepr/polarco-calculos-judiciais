
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from backend.app.adapters.orm.models.base import Base
from backend.app.adapters.orm.models.association_tables import company_user
from backend.app.adapters.orm.models.user import User

class Company(Base):
    __tablename__ = 'company'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    members: Mapped[List['User']] = relationship(
        'User',
        secondary=company_user,
        back_populates='companies',
        lazy='selectin'
    )