import uuid
from pydantic import BaseModel, Field
from typing import List, Optional

class CompanyBase(BaseModel):
    name: str
    cnpj: str = Field(..., min_length=14, max_length=18)
    is_active: bool = True

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    cnpj: str
    is_active: bool

class CompanyDetail(CompanyResponse):
    members: List[int] = []