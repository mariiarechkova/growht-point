from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.database import Base


class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    stability = Column(Float, default=1.5)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Organisation name={self.name}>"
