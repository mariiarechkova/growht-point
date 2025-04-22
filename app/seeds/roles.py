from sqlalchemy import select

from app.core.database import async_session_maker
from app.users.models import Role


async def seed_roles():
    async with async_session_maker() as session:
        result = await session.execute(select(Role).where(Role.title == "admin"))
        role = result.scalar_one_or_none()

        if not role:
            session.add(Role(title="admin"))
            await session.commit()
            print("Role 'admin' created")
        else:
            print("Role 'admin' already exists")
