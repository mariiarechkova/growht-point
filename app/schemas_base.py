from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DepartmentRead(BaseModel):
    id: int
    title: str
    organisation_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
