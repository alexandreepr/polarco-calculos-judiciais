from sqlalchemy import String, Boolean, DateTime, ForeignKey
import uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.adapters.orm.models.base import Base

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    user = relationship('User')