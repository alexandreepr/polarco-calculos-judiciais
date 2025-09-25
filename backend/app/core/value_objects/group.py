from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

from .role import RoleResponse
from .user import UserResponse

class GroupDetails(GroupResponse):
    users: List[UserResponse] = []
    roles: List[RoleResponse] = []

    model_config = ConfigDict(from_attributes=True)

GroupDetails.model_rebuild()
