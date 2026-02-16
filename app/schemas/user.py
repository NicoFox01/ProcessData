from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.enums import UserRole, Vertical

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    vertical: Optional[Vertical] = None
    is_active:bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    vertical: Optional[Vertical] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)