from sqlalchemy.orm import DeclarativeBase


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
