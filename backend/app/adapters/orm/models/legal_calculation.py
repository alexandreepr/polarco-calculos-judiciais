from typing import List, Optional
import uuid
from datetime import date
from enum import Enum as PyEnum

from sqlalchemy import Date, Float, ForeignKey, Integer, JSON, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.orm.models.base import Base
from app.adapters.orm.models.legal_case import LegalCase
from app.adapters.orm.models.user import User


class MonetaryIndexType(PyEnum):
    IPCA = "IPCA"
    INPC = "INPC"
    IGP_M = "IGP-M"
    OTHER = "OTHER"


class InterestIndexType(PyEnum):
    ONE_PERCENT = "1_PERCENT"      # juros de mora 1%
    SELIC = "SELIC"               # juros Selic
    LEGAL_RATE = "LEGAL_RATE"     # taxa legal
    OTHER = "OTHER"


class LegalCalculation(Base):
    __tablename__ = "legal_calculations"

    id: Mapped[uuid.UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    calculation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    # relation to the legal case
    legal_case_id: Mapped[uuid.UUID] = mapped_column(
        String(36), ForeignKey("legal_cases.id"), nullable=False, index=True
    )
    legal_case: Mapped["LegalCase"] = relationship("LegalCase", backref="calculations")

    # basic calculation metadata
    calculation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # payments: number of payments, optional explicit list of payment dates and amounts
    number_of_payments: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    payment_dates: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # list of ISO date strings
    payment_amounts: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # list of floats

    # moral (non-pecuniary) damage fields
    nominal_moral_damage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    moral_interest_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    moral_index_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    moral_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    moral_index_type: Mapped[Optional[MonetaryIndexType]] = mapped_column(
        SQLEnum(MonetaryIndexType, native_enum=False), nullable=True
    )
    moral_interest_index_type: Mapped[Optional[InterestIndexType]] = mapped_column(
        SQLEnum(InterestIndexType, native_enum=False), nullable=True
    )

    corrected_moral_value: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    moral_interest_value: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    moral_total_updated_value: Mapped[Optional[float]] = mapped_column(Float, default=0.0)

    accumulated_moral_index: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    accumulated_moral_interest_1pct: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    accumulated_moral_interest_selic: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    accumulated_moral_interest_legal: Mapped[Optional[float]] = mapped_column(Float, default=0.0)

    # material (pecuniary) damage fields
    nominal_material_damage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    material_interest_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    material_index_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    material_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    material_index_type: Mapped[Optional[MonetaryIndexType]] = mapped_column(
        SQLEnum(MonetaryIndexType, native_enum=False), nullable=True
    )
    material_interest_index_type: Mapped[Optional[InterestIndexType]] = mapped_column(
        SQLEnum(InterestIndexType, native_enum=False), nullable=True
    )

    corrected_material_value: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    material_interest_value: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    material_total_updated_value: Mapped[Optional[float]] = mapped_column(Float, default=0.0)

    total_judgement_amount: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    total_judgment_without_interest: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    total_interest_amount: Mapped[Optional[float]] = mapped_column(Float, default=0.0)

    # who created this calculation
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    created_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by_id])

    def __repr__(self) -> str:
        return f"<LegalCalculation id={self.id} legal_case_id={self.legal_case_id}>"