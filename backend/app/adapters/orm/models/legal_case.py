from datetime import date
from typing import List, Optional
import uuid
from enum import Enum as PyEnum
from sqlalchemy import JSON, UUID, Date, Float, ForeignKey, String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.orm.models.user import User

from .base import Base

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

class MaterialResolutionType(PyEnum):
    ANNULLED = "ANNULLED"     # ANULADO
    CONVERTED = "CONVERTED"   # CONVERTIDO

class InterestMultiplierType(PyEnum):
    SIMPLE = "SIMPLE"         # SIMPLES
    DOUBLED = "DOUBLED"       # DOBRADO

class CaseValueBasisType(PyEnum):
    CONDEMNATION_AMOUNT = "CONDEMNATION_AMOUNT"  # VALOR DA CONDENAÇÃO
    CLAIM_AMOUNT = "CLAIM_AMOUNT"                # VALOR DA CAUSA
    SPECIFIED_AMOUNT = "SPECIFIED_AMOUNT"        # QUANTIA CERTA

class LegalCase(Base):
    __tablename__ = 'legal_cases'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    legal_case_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    case_subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    judicial_district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    court: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    defendant: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    attorney: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    clients: Mapped[Optional[list[dict]]] = mapped_column(JSON, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # legal case dates (juridical)
    filing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)                # DATA DE AJUIZAMENTO
    citation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)              # DATA DA CITAÇÃO (service)
    damage_event_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)          # DATA DO EVENTO DANOSO
    judgment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)              # DATA DA SENTENÇA
    appellate_decision_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)    # DATA DO ACÓRDÃO
    final_judgment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)        # DATA DO TRÂNSITO EM JULGADO

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
    material_resolution: Mapped[Optional[MaterialResolutionType]] = mapped_column(
        SQLEnum(MaterialResolutionType, native_enum=False), nullable=True
    )  # ANULADO / CONVERTIDO
    material_interest_multiplier: Mapped[Optional[InterestMultiplierType]] = mapped_column(
        SQLEnum(InterestMultiplierType, native_enum=False), nullable=True
    )  # SIMPLES / DOBRADO

    # installment / payment-specific fields for material damages
    first_installment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)        # DATA DA PRIMEIRA PARCELA
    last_installment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)         # DATA DA ÚLTIMA PARCELA
    first_installment_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)    # VALOR DA PRIMEIRA PARCELA
    last_installment_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)     # VALOR DA ÚLTIMA PARCELA
    
    # case value and attorney fees
    case_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    case_value_basis: Mapped[Optional[CaseValueBasisType]] = mapped_column(
        SQLEnum(CaseValueBasisType, native_enum=False), nullable=True
    )
    attorney_fees_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    percentage_court_awarded_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True)
    proportion_court_awarded_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True)
    percentage_contractual_attorney_fees: Mapped[Optional[float]] = mapped_column(nullable=True)

    created_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    deleted_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    deleted_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[deleted_by_id])
    
    assignee_from_juridical_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    assignee_from_juridical_team: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[assignee_from_juridical_team_id]
    )

    assignee_from_litigation_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    assignee_from_litigation_team: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[assignee_from_litigation_team_id]
    )

