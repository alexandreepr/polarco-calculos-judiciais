import uuid
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field

class LegalCaseBase(BaseModel):
    legal_case_number: str
    case_value: Optional[float] = None
    attorney_fees_value: Optional[float] = None
    percentage_court_awarded_attorney_fees: Optional[float] = None
    proportion_court_awarded_attorney_fees: Optional[float] = None
    percentage_contractual_attorney_fees: Optional[float] = None
    case_subject: Optional[str] = None
    state: Optional[str] = None
    jurisdiction: Optional[str] = None
    judicial_district: Optional[str] = None
    court: Optional[str] = None
    defendant: Optional[str] = None
    attorney: Optional[str] = None
    clients: Optional[List[Dict[str, str]]] = None  # List of dicts with name/cpf
    status: Optional[str] = None

    assignee_from_commercial_team_id: Optional[uuid.UUID] = None
    assignee_from_litigation_team_id: Optional[uuid.UUID] = None

class LegalCaseCreate(LegalCaseBase):
    pass

class LegalCaseUpdate(LegalCaseBase):
    pass

class LegalCaseResponse(LegalCaseBase):
    id: uuid.UUID = Field(...)
    model_config = ConfigDict(from_attributes=True)