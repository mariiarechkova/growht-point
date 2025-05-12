from faker import Faker
from sqlalchemy import select

from app.core.database import async_session_maker
from app.core.security import hash_password
from app.organisation.models import Organisation
from app.users.models import Role, User
from app.voting.models import MainVoteEvent


faker = Faker()


async def seed_admin_org():
    async with async_session_maker() as session:
        try:
            async with session.begin():

                org_name = faker.company()
                organisation = Organisation(name=org_name)
                organisation.main_vote_event = MainVoteEvent()
                session.add(organisation)

                result = await session.execute(select(Role).where(Role.title == "admin"))
                admin_role = result.scalar_one_or_none()

                if not admin_role:
                    raise Exception("Admin role not found!")

                first_name = faker.first_name()
                last_name = faker.last_name()
                email = f"{first_name}.{last_name}@admin.com"
                password = "admin123"
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    hashed_password=hash_password(password),
                    organisation=organisation,
                )

                user.roles.append(admin_role)
                session.add(user)

            print(f"Created organisation '{org_name}' and admin user: {email}")

        except Exception as e:
            print(f"Error: {e}")
