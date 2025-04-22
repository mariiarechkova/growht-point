from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..core.security import hash_password
from .models import User
from .schemas import UserCreate


# from .schemas import UserRead


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, org_id: int) -> list[User]:
        result = await self.session.execute(
            select(User).options(selectinload(User.roles)).where(User.organisation_id == org_id)
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
