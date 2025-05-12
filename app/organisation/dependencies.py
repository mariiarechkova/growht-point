from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session

from .repository import DepartmentRepository, OrganisationRepository
from .services.common_services import DepartmentService, OrganisationService


async def get_organisation_service(
    session: AsyncSession = Depends(get_session),
) -> OrganisationService:
    repo = OrganisationRepository(session)
    return OrganisationService(repo)


def get_department_service(
    session: AsyncSession = Depends(get_session),
) -> DepartmentService:
    repo = DepartmentRepository(session)
    return DepartmentService(repo)
