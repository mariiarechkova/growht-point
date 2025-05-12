from enum import Enum

from pydantic import BaseModel


class Frequency(str, Enum):
    week = "week"
    month = "month"
    quarter = "quarter"
    year = "year"


class VoteEventRead(BaseModel):
    id: int
    frequency: Frequency
    organisation_id: int

    model_config = {"from_attributes": True}
