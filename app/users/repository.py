from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


# from .schemas import UserRead


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int):
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
