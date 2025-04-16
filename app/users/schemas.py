from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr


class RoleRead(BaseModel):
    id: int
    title: str
    weight_vote: Optional[Decimal] = None

    model_config = {"from_attributes": True}


def empty_list() -> list:
    return []


class UserRead(UserBase):
    id: int
    is_finish_sign_up: bool
    is_approve_role: bool
    created_at: datetime
    # roles: Optional[List[RoleRead]] = None

    model_config = {"from_attributes": True}

    # class Config:
    #     # Сортировка полей по порядку
    #     json_encoders = {
    #         'id': 'first',  # это по-умолчанию .
    #     }


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
