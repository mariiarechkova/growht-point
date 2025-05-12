from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum

from app.core.database import Base
from app.voting.schemas import Frequency


class MainVoteEvent(Base):
    __tablename__ = "main_vote_event"

    id = Column(Integer, primary_key=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), nullable=False, unique=True)
    frequency = Column(SqlEnum(Frequency, name="frequency_enum"), nullable=False, default=Frequency.month)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # relations
    organisation = relationship("Organisation", back_populates="main_vote_event")
