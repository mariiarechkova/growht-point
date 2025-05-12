from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.users.schemas import UserCreate, UserRead


class OrganisationBase(BaseModel):
    name: str = Field(..., max_length=255)
    stability: float = Field(default=1.5, gt=1, lt=2)


class OrganisationAndUserCreate(OrganisationBase):
    user: UserCreate


class OrganisationRead(OrganisationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrganisationUpdate(BaseModel):
    stability: float = Field(..., gt=1, lt=2)


class OrganisationWithUser(BaseModel):
    organisation: OrganisationRead
    user: UserRead

    model_config = ConfigDict(from_attributes=True)


class DepartmentCreate(BaseModel):
    title: str = Field(..., max_length=255)
    organisation_id: int

    model_config = ConfigDict(from_attributes=True)


class DepartmentRead(BaseModel):
    id: int
    title: str
    organisation_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentUpdate(BaseModel):
    title: str = Field(..., max_length=255)
