from __future__ import annotations
from typing import List, Optional
import uuid
from datetime import date
from pydantic import BaseModel, Field
from app.adapters.orm.models.legal_calculation import MonetaryIndexType, InterestIndexType


class LegalCalculationBase(BaseModel):
    calculation_type: Optional[str] = Field(None, description="Type of calculation (e.g. 'moral', 'material', etc.)")
    calculation_date: Optional[date] = None
    description: Optional[str] = None

    # payments
    number_of_payments: Optional[int] = None
    payment_dates: Optional[List[date]] = None
    payment_amounts: Optional[List[float]] = None

    # moral (non-pecuniary) damage
    nominal_moral_damage: Optional[float] = None
    moral_interest_start_date: Optional[date] = None
    moral_index_start_date: Optional[date] = None
    moral_end_date: Optional[date] = None
    moral_index_type: Optional[MonetaryIndexType] = None
    moral_interest_index_type: Optional[InterestIndexType] = None
    corrected_moral_value: Optional[float] = None
    moral_interest_value: Optional[float] = None
    moral_total_updated_value: Optional[float] = None
    accumulated_moral_index: Optional[float] = None
    accumulated_moral_interest_1pct: Optional[float] = None
    accumulated_moral_interest_selic: Optional[float] = None
    accumulated_moral_interest_legal: Optional[float] = None

    # material (pecuniary) damage
    nominal_material_damage: Optional[float] = None
    material_interest_start_date: Optional[date] = None
    material_index_start_date: Optional[date] = None
    material_end_date: Optional[date] = None
    material_index_type: Optional[MonetaryIndexType] = None
    material_interest_index_type: Optional[InterestIndexType] = None
    corrected_material_value: Optional[float] = None
    material_interest_value: Optional[float] = None
    material_total_updated_value: Optional[float] = None

    class Config:
        extra = "forbid"


class LegalCalculationCreate(LegalCalculationBase):
    legal_case_id: uuid.UUID = Field(..., description="Related legal case id")
    # created_by_id will be set by use-case from current_user


class LegalCalculationUpdate(BaseModel):
    # all fields optional; exclude_unset will be used by use-case
    calculation_type: Optional[str] = None
    calculation_date: Optional[date] = None

    number_of_payments: Optional[int] = None
    payment_dates: Optional[List[date]] = None
    payment_amounts: Optional[List[float]] = None

    nominal_moral_damage: Optional[float] = None
    moral_interest_start_date: Optional[date] = None
    moral_index_start_date: Optional[date] = None
    moral_end_date: Optional[date] = None
    moral_index_type: Optional[MonetaryIndexType] = None
    moral_interest_index_type: Optional[InterestIndexType] = None
    corrected_moral_value: Optional[float] = None
    moral_interest_value: Optional[float] = None
    moral_total_updated_value: Optional[float] = None
    accumulated_moral_index: Optional[float] = None
    accumulated_moral_interest_1pct: Optional[float] = None
    accumulated_moral_interest_selic: Optional[float] = None
    accumulated_moral_interest_legal: Optional[float] = None

    nominal_material_damage: Optional[float] = None
    material_interest_start_date: Optional[date] = None
    material_index_start_date: Optional[date] = None
    material_end_date: Optional[date] = None
    material_index_type: Optional[MonetaryIndexType] = None
    material_interest_index_type: Optional[InterestIndexType] = None
    corrected_material_value: Optional[float] = None
    material_interest_value: Optional[float] = None
    material_total_updated_value: Optional[float] = None

    class Config:
        extra = "forbid"


class LegalCalculationResponse(LegalCalculationBase):
    id: uuid.UUID
    legal_case_id: uuid.UUID
    created_by_id: Optional[uuid.UUID] = None
    # if your Base model includes timestamps:
    created_at: Optional[date] = None
    updated_at: Optional[date] = None

    model_config = {"from_attributes": True}