from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Department, Organisation
from .schemas import DepartmentCreate, DepartmentUpdate, OrganisationUpdate


class OrganisationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Organisation]:
        result = await self.session.execute(select(Organisation))
        return result.scalars().all()

    async def get_by_id(self, org_id: int) -> Organisation:
        result = await self.session.execute(select(Organisation).where(Organisation.id == org_id))
        organisation = result.scalar_one_or_none()
        if organisation is None:
            raise HTTPException(status_code=404, detail="Organisation not found")
        return organisation

    async def update(self, org_id: int, org_in: OrganisationUpdate) -> Organisation:
        organisation = await self.get_by_id(org_id)
        organisation.stability = org_in.stability
        await self.session.commit()
        await self.session.refresh(organisation)
        return organisation

    async def delete(self, org_id: int) -> None:
        organisation = await self.get_by_id(org_id)
        await self.session.delete(organisation)
        await self.session.commit()


class DepartmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Department]:
        result = await self.session.execute(select(Department))
        return result.scalars().all()

    async def get_by_id(self, dept_id: int) -> Department:
        result = await self.session.execute(select(Department).where(Department.id == dept_id))
        department = result.scalar_one_or_none()
        if department is None:
            raise HTTPException(status_code=404, detail="Department not found")
        return department

    async def create(self, dept_in: DepartmentCreate) -> Department:
        department = Department(**dept_in.model_dump())
        self.session.add(department)
        await self.session.commit()
        await self.session.refresh(department)
        return department

    async def update(self, dept_id: int, dept_in: DepartmentUpdate) -> Department:
        department = await self.get_by_id(dept_id)
        department.title = dept_in.title
        await self.session.commit()
        await self.session.refresh(department)
        return department

    async def delete(self, dept_id: int) -> None:
        department = await self.get_by_id(dept_id)
        await self.session.delete(department)
        await self.session.commit()
