from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    stability = Column(Float, default=1.5)
    created_at = Column(DateTime, default=datetime.utcnow)

    departments = relationship("Department", back_populates="organisation")
    users = relationship("User", back_populates="organisation")
    main_vote_event = relationship("MainVoteEvent", back_populates="organisation", uselist=False)

    def __repr__(self):
        return f"<Organisation name={self.name}>"


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), nullable=False)

    organisation = relationship("Organisation", back_populates="departments")
    users = relationship("User", back_populates="departments")

    def __repr__(self):
        return f"<Organisation title={self.title}, organisation_id={self.organisation_id}>"
