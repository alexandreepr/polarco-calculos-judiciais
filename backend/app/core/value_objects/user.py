from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import List

from .group import GroupResponse
from .role import RoleResponse

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def password_strength(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain at least one uppercase letter')
        return password

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDetails(UserResponse):
    roles: List["RoleResponse"] = []
    groups: List["GroupResponse"] = []

    model_config = ConfigDict(from_attributes=True)

UserDetails.model_rebuild()
