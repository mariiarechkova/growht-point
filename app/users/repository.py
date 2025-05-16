from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import hash_password
from .models import User
from .schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, org_id: int, order_by: str, order: str):
        order_func = asc if order == "asc" else desc
        column = getattr(User, order_by)
        result = await self.session.execute(
            select(User).where(User.organisation_id == org_id).order_by(order_func(column))
        )
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_user_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, data: UserCreate, organisation_id: int) -> User:
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            hashed_password=hash_password(data.password),
            organisation_id=organisation_id,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
