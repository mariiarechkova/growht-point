from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    weight_vote = Column(Float)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    users = relationship("User", secondary=user_roles, back_populates="roles", lazy="selectin")

    def __repr__(self):
        return f"Title {self.title}"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    is_finish_sign_up = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    weight_vote = Column(Float)
    is_approve_role = Column(Boolean, default=False)
    is_available_re_vote = Column(Boolean, default=False)

    department_id = Column(Integer, ForeignKey("departments.id"))
    organisation_id = Column(Integer, ForeignKey("organisations.id"))

    # Relationships
    departments = relationship("Department", back_populates="users")
    organisation = relationship("Organisation", back_populates="users")
    profile = relationship("Profile", back_populates="user", uselist=False, lazy="selectin")
    roles = relationship("Role", secondary=user_roles, back_populates="users", lazy="selectin")

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.email})>"


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    image = Column(String(255))
    job_title = Column(String(100))
    description = Column(Text)
    salary = Column(Numeric(precision=10, scale=2))
    start_work_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="profile")
