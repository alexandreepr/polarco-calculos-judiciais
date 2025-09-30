from typing import List, Optional
import uuid
from sqlalchemy import JSON, UUID, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.orm.models.user import User

from .base import Base

class LegalCase(Base):
    __tablename__ = 'legal_cases'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    legal_case_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    case_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    attorney_fees_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    percentage_court_awarded_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True)
    proportion_court_awarded_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True)
    percentage_contractual_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True)
    case_subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    judicial_district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    court: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    defendant: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    attorney: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    clients: Mapped[Optional[list[dict]]] = mapped_column(JSON, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    deleted_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    deleted_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[deleted_by_id])
    assignee_from_commercial_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    assignee_from_commercial_team: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[assignee_from_commercial_team_id]
    )

    assignee_from_litigation_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    assignee_from_litigation_team: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[assignee_from_litigation_team_id]
    )

