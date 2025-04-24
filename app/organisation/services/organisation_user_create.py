from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.organisation.models import Organisation
from app.organisation.schemas import OrganisationAndUserCreate, OrganisationRead
from app.users.models import Role
from app.users.repository import UserRepository
from app.users.schemas import UserRead
from app.utils.email_sender import send_welcome_email


class OrganisationUserCreatorService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._user_repo = UserRepository(session)

    async def create(self, data: OrganisationAndUserCreate):
        try:
            async with self._session.begin():
                organisation = Organisation(name=data.name, created_at=datetime.utcnow())
                self._session.add(organisation)
                await self._session.flush()

                user = await self._user_repo.create_user(data.user, organisation_id=organisation.id)
                result = await self._session.execute(select(Role).where(Role.title == "admin"))
                admin_role = result.scalar_one_or_none()

                if not admin_role:
                    raise Exception("Admin role not found!")

                user.roles.append(admin_role)
                await self._session.flush()

                await self._session.refresh(user, attribute_names=["roles"])
                await self._session.refresh(organisation)

                try:
                    await send_welcome_email(user.email, user.first_name)
                except Exception as email_err:
                    print(f"[WARN] Couldn't send email: {email_err}")

                return (
                    OrganisationRead.model_validate(organisation),
                    UserRead.model_validate(user),
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Organization creation error: {e}")
