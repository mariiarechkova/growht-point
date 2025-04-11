from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session

from .repository import DepartmentRepository, OrganisationRepository


def get_organisation_repository(
    session: AsyncSession = Depends(get_session),
) -> OrganisationRepository:
    return OrganisationRepository(session)


def get_department_repository(
    session: AsyncSession = Depends(get_session),
) -> DepartmentRepository:
    return DepartmentRepository(session)
