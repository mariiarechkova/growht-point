import pytest
from fastapi import HTTPException

from app.organisation.models import Department, Organisation
from app.organisation.repository import DepartmentRepository, OrganisationRepository
from app.organisation.schemas import DepartmentCreate, DepartmentUpdate, OrganisationUpdate


@pytest.mark.asyncio
async def test_get_all_organisations(async_session):
    repo = OrganisationRepository(async_session)
    async_session.add_all([Organisation(name="Org1"), Organisation(name="Org2")])
    await async_session.commit()

    result = await repo.get_all()
    assert len(result) == 2
    assert result[0].name == "Org1"
    assert result[1].name == "Org2"


@pytest.mark.asyncio
async def test_get_by_id_found(async_session):
    repo = OrganisationRepository(async_session)
    org = Organisation(name="TestOrg")
    async_session.add(org)
    await async_session.commit()

    found = await repo.get_by_id(org.id)
    assert found.name == "TestOrg"


@pytest.mark.asyncio
async def test_get_by_id_not_found(async_session):
    repo = OrganisationRepository(async_session)
    with pytest.raises(HTTPException) as exc_info:
        await repo.get_by_id(999)
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_organisation(async_session):
    repo = OrganisationRepository(async_session)
    org = Organisation(name="ToUpdate", stability=1)
    async_session.add(org)
    await async_session.commit()

    update = OrganisationUpdate(stability=1.5)
    updated = await repo.update(org.id, update)
    assert updated.stability == 1.5


@pytest.mark.asyncio
async def test_delete_organisation(async_session):
    repo = OrganisationRepository(async_session)
    org = Organisation(name="ToDelete")
    async_session.add(org)
    await async_session.commit()

    await repo.delete(org.id)
    result = await repo.get_all()
    assert len(result) == 0


@pytest.mark.asyncio
async def test_get_all_department(async_session, test_organisation):
    repo = DepartmentRepository(async_session)
    async_session.add_all(
        [
            Department(title="it", organisation_id=test_organisation.id),
            Department(title="management", organisation_id=test_organisation.id),
        ]
    )
    await async_session.commit()

    result = await repo.get_all()
    assert len(result) == 2
    assert result[0].title == "it"
    assert result[1].title == "management"


@pytest.mark.asyncio
async def test_get_department_by_id_found(async_session, test_organisation):
    repo = DepartmentRepository(async_session)
    dept = Department(title="TestDept", organisation_id=test_organisation.id)
    async_session.add(dept)
    await async_session.commit()

    found = await repo.get_by_id(dept.id)
    assert found.title == "TestDept"


@pytest.mark.asyncio
async def test_get_department_by_id_not_found(async_session):
    repo = DepartmentRepository(async_session)
    with pytest.raises(HTTPException) as exc_info:
        await repo.get_by_id(999)
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_create_department(async_session, test_organisation):
    repo = DepartmentRepository(async_session)
    dept_in = DepartmentCreate(title="TestDept", organisation_id=test_organisation.id)
    department = await repo.create(dept_in)

    assert department.id is not None
    assert department.title == "TestDept"
    assert department.organisation_id == test_organisation.id


@pytest.mark.asyncio
async def test_update_department(async_session, test_organisation):
    repo = DepartmentRepository(async_session)
    dept = Department(title="TestDept", organisation_id=test_organisation.id)
    async_session.add(dept)
    await async_session.commit()

    update = DepartmentUpdate(title="NewTestDept")
    updated = await repo.update(dept_id=dept.id, dept_in=update)
    assert updated.title == "NewTestDept"


@pytest.mark.asyncio
async def test_delete_department(async_session, test_organisation):
    repo = DepartmentRepository(async_session)
    dept = Department(title="TestDept", organisation_id=test_organisation.id)
    async_session.add(dept)
    await async_session.commit()

    await repo.delete(dept.id)
    result = await repo.get_all()
    assert len(result) == 0
