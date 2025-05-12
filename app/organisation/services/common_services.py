from app.organisation.repository import DepartmentRepository, OrganisationRepository


class OrganisationService:
    def __init__(self, repo: OrganisationRepository):
        self._repo = repo

    async def get_all(self):
        return await self._repo.get_all()

    async def get_by_id(self, org_id: int):
        return await self._repo.get_by_id(org_id)

    async def update(self, org_id, org_in):
        return await self._repo.update(org_id, org_in)

    async def delete(self, org_id):
        return await self._repo.delete(org_id)


class DepartmentService:
    def __init__(self, repo: DepartmentRepository):
        self._repo = repo

    async def get_all(self):
        return await self._repo.get_all()

    async def get_by_id(self, dept_id: int):
        return await self._repo.get_by_id(dept_id)

    async def create(self, dept_in):
        return await self._repo.create(dept_in)

    async def update(self, dept_id, dept_in):
        return await self._repo.update(dept_id, dept_in)

    async def delete(self, dept_id):
        return await self._repo.delete(dept_id)
