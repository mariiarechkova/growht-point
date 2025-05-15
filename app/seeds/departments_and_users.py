from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.organisation.models import Department, Organisation
from app.users.models import User


faker = Faker()


async def seed_departments_with_users(session: AsyncSession):
    organisation = await session.scalar(select(Organisation).order_by(Organisation.id.desc()).limit(1))
    if not organisation:
        raise ValueError("No organisation found.")

    dept_titles = ["HR", "Engineering", "Marketing", "Sales", "Product"]

    departments = []

    for title in dept_titles:
        dept = Department(title=title, organisation_id=organisation.id)
        session.add(dept)
        departments.append(dept)

    await session.flush()

    for department in departments:
        for _ in range(2):
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = f"{first_name}.{last_name}@user.com"
            password = "password123"
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                hashed_password=hash_password(password),
                organisation=organisation,
                department_id=department.id,
            )
            session.add(user)

    print("All done: 5 departments × 2 users each")
