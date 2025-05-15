from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.organisation.models import Organisation
from app.seeds.roles import seed_roles
from app.users.models import User
from app.voting.models import MainVoteEvent


faker = Faker()


async def seed_admin_org(session: AsyncSession):
    admin_role = await seed_roles(session)

    org_name = faker.company()
    organisation = Organisation(name=org_name)
    organisation.main_vote_event = MainVoteEvent()
    session.add(organisation)

    first_name = faker.first_name()
    last_name = faker.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@admin.com"
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
