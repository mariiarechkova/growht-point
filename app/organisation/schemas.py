from datetime import datetime

from pydantic import BaseModel, Field


class OrganisationBase(BaseModel):
    name: str = Field(..., max_length=255)
    stability: float = Field(default=1.5, gt=1, lt=2)


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationRead(OrganisationBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class OrganisationUpdate(BaseModel):
    stability: float = Field(..., gt=1, lt=2)


class DepartmentCreate(BaseModel):
    title: str = Field(..., max_length=255)
    organisation_id: int

    model_config = {"from_attributes": True}


class DepartmentRead(BaseModel):
    id: int
    title: str
    organisation_id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class DepartmentUpdate(BaseModel):
    title: str = Field(..., max_length=255)
