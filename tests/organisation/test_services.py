from unittest.mock import AsyncMock, patch

import pytest

from app.organisation.models import Department, Organisation
from app.organisation.schemas import DepartmentCreate, DepartmentUpdate, OrganisationAndUserCreate, OrganisationUpdate
from app.organisation.services.common_services import DepartmentService, OrganisationService
from app.organisation.services.organisation_user_create import OrganisationUserCreatorService
from app.users.models import Role
from app.users.schemas import UserCreate


@pytest.fixture
def mock_organisation_repo():
    repo = AsyncMock()
    repo.get_all.return_value = [
        Organisation(id=1, name="Org1"),
        Organisation(id=2, name="Org2"),
    ]
    repo.get_by_id.return_value = Organisation(id=1, name="Org1")
    repo.update.return_value = Organisation(id=1, name="Org1", stability=1.7)
    return repo


@pytest.mark.asyncio
async def test_get_all_organisations_service(mock_organisation_repo):
    service = OrganisationService(mock_organisation_repo)

    result = await service.get_all()

    assert len(result) == 2
    assert result[0].name == "Org1"
    mock_organisation_repo.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_org_by_id_service(mock_organisation_repo):
    service = OrganisationService(mock_organisation_repo)

    result = await service.get_by_id(1)

    assert result.name == "Org1"
    mock_organisation_repo.get_by_id.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_org_service(mock_organisation_repo):
    service = OrganisationService(mock_organisation_repo)
    org_in = OrganisationUpdate(stability=1.7)

    result = await service.update(1, org_in)

    assert isinstance(result, Organisation)
    assert result.stability == 1.7
    mock_organisation_repo.update.assert_awaited_once_with(1, org_in)


@pytest.mark.asyncio
async def test_delete_org_service(mock_organisation_repo):
    service = OrganisationService(mock_organisation_repo)

    await service.delete(1)
    mock_organisation_repo.delete.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.organisation.services.organisation_user_create.send_welcome_email", new_callable=AsyncMock)
async def test_create_organisation_user(mock_send_email, async_session):
    # Подготовка: создаём роль "admin"
    role = Role(title="admin")
    async_session.add(role)
    await async_session.commit()

    # Создаём входной DTO
    org_dto = OrganisationAndUserCreate(
        name="TestOrg",
        user=UserCreate(first_name="Test", last_name="User", email="test@example.com", password="testpass123"),
    )

    # Создаём сервис
    service = OrganisationUserCreatorService(async_session)

    # Вызываем метод create
    org_out, user_out = await service.create(org_dto)

    # Проверки результата
    assert org_out.name == "TestOrg"
    assert user_out.email == "test@example.com"
    assert user_out.first_name == "Test"
    assert any(role.title == "admin" for role in user_out.roles)

    # Проверка вызова email
    mock_send_email.assert_called_once_with("test@example.com", "Test")


@pytest.fixture
def mock_department_repo():
    repo = AsyncMock()
    repo.get_all.return_value = [
        Department(id=1, title="Dept1", organisation_id=1),
        Department(id=2, title="Dept2", organisation_id=1),
    ]
    repo.get_by_id.return_value = Department(id=1, title="Dept1", organisation_id=1)
    repo.update.return_value = Department(id=1, title="NewDept1", organisation_id=1)
    repo.create.return_value = Department(id=3, title="Dept3", organisation_id=1)
    return repo


@pytest.mark.asyncio
async def test_get_all_department_service(mock_department_repo):
    service = DepartmentService(mock_department_repo)

    result = await service.get_all()

    assert len(result) == 2
    assert result[0].title == "Dept1"
    mock_department_repo.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_dept_by_id_service(mock_department_repo):
    service = DepartmentService(mock_department_repo)

    result = await service.get_by_id(1)

    assert result.title == "Dept1"
    mock_department_repo.get_by_id.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_dept_by_id_service(mock_department_repo):
    service = DepartmentService(mock_department_repo)

    dept_in = DepartmentCreate(title="Dept3", organisation_id=1)
    result = await service.create(dept_in)
    assert result.title == "Dept3"
    mock_department_repo.create.assert_awaited_once_with(dept_in)


@pytest.mark.asyncio
async def test_update_dept_service(mock_department_repo):
    service = DepartmentService(mock_department_repo)
    dept_in = DepartmentUpdate(title="NewDept1")

    result = await service.update(1, dept_in)

    assert isinstance(result, Department)
    assert result.title == "NewDept1"
    mock_department_repo.update.assert_awaited_once_with(1, dept_in)


@pytest.mark.asyncio
async def test_delete_dept_service(mock_department_repo):
    service = DepartmentService(mock_department_repo)

    await service.delete(1)
    mock_department_repo.delete.assert_awaited_once()
