from sqlalchemy import select

from app.users.models import Role
from app.users.schemas import RoleEnum


async def seed_roles(session):
    result = await session.execute(select(Role).where(Role.title == RoleEnum.ADMIN))
    role = result.scalar_one_or_none()

    if not role:
        role = Role(title=RoleEnum.ADMIN)
        session.add(role)
        await session.flush()  # use flash instead of commit
        print("Role 'admin' created")
    else:
        print("Role 'admin' already exists")

    return role
