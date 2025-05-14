from sqlalchemy import select

from app.users.models import Role


async def seed_roles(session):
    result = await session.execute(select(Role).where(Role.title == "admin"))
    role = result.scalar_one_or_none()

    if not role:
        role = Role(title="admin")
        session.add(role)
        await session.flush()  # 👈 используем flush вместо commit
        print("Role 'admin' created")
    else:
        print("Role 'admin' already exists")

    return role
