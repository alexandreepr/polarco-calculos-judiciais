from typing import List, Optional
from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.orm.models.user import User

from .base import Base

class LegalCase(Base):
    __tablename__ = 'legal_cases'

    legal_case_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    case_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    attorney_fees_value: Mapped[Optional[float]] = mapped_column(nullable=True) # valor honorários advocatícios
    percentage_court_awarded_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True) # percentual honorários advocatícios fixados pelo juízo
    proportion_court_awarded_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True) # proporção honorários advocatícios fixados pelo juízo
    percentage_contractual_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True) # percentual honorários advocatícios contratuais
    case_subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # matéria [definir valores possiveis]
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # estado
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # foro
    judicial_district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # comarca
    court: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # vara
    defendant: Mapped[Optional[str]] = mapped_column(String(200), nullable=True) # réu
    attorney: Mapped[Optional[str]] = mapped_column(String(200), nullable=True) # advogado
    clients: Mapped[Optional[list[dict]]] = mapped_column(JSON, nullable=True)
    assignee_from_commercial_team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    assignee_from_commercial_team: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[assignee_from_commercial_team_id]
    )
    assignee_from_litigation_team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    assignee_from_litigation_team: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[assignee_from_litigation_team_id]
    )
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # status [definir valores possiveis]
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    deleted_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    deleted_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[deleted_by_id])

