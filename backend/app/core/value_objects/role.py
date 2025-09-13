from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from .permission import PermissionResponse

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoleDetails(RoleResponse):
    permissions: List["PermissionResponse"] = []

    model_config = ConfigDict(from_attributes=True)

RoleDetails.model_rebuild()
