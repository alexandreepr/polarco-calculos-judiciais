from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional

class PermissionBase(BaseModel):
    name: str
    resource: str
    action: str
    description: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)