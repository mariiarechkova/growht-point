from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RoleEnum(str, Enum):
    ADMIN = "admin"


class UserBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr


class RoleRead(BaseModel):
    id: int
    title: RoleEnum
    weight_vote: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


class ProfileRead(BaseModel):
    id: int
    job_title: Optional[str] = None
    salary: Optional[Decimal] = None


class UserRead(UserBase):
    id: int
    is_finish_sign_up: bool
    is_approve_role: bool
    created_at: datetime
    profile: ProfileRead
    department_id: Optional[int] = None
    roles: List[RoleRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class SendMassage(BaseModel):
    type: str
    value: str
    text: str
