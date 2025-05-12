import pytest
import pytest_asyncio
from fastapi import status
from sqlalchemy import insert

from app.main import app
from app.organisation.models import Department, Organisation
from app.users.dependencies import require_admin_user
from app.users.models import Role


@pytest_asyncio.fixture
async def seeded_organisations(async_session):
    orgs = [
        Organisation(name="Org1"),
        Organisation(name="Org2"),
    ]
    async_session.add_all(orgs)
    await async_session.commit()
    return orgs


@pytest.fixture
def override_admin_auth():
    app.dependency_overrides[require_admin_user] = lambda: None
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_orgs_router(client, seeded_organisations):
    # Отправляем запрос
    response = await client.get("/api/organisations/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_organisation_by_id(client, seeded_organisations):
    response = await client.get("/api/organisations/1")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Org1"


@pytest.mark.asyncio
async def test_create_organisation_with_user_router(client, async_session):
    # Подготовка: добавим роль 'admin', иначе сервис упадёт
    await async_session.execute(insert(Role).values(title="admin"))
    await async_session.commit()

    # Запрос
    response = await client.post(
        "/api/organisations/",
        json={
            "name": "TestOrg",
            "user": {
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice@example.com",
                "password": "secret123",
            },
        },
    )

    # Проверки
    assert response.status_code == 201
    data = response.json()

    assert data["organisation"]["name"] == "TestOrg"
    assert data["user"]["email"] == "alice@example.com"
    assert data["user"]["first_name"] == "Alice"
    assert "roles" in data["user"]
    assert any(role["title"] == "admin" for role in data["user"]["roles"])


@pytest.mark.asyncio
async def test_update_organisation_router(client, seeded_organisations, override_admin_auth):
    response = await client.patch("/api/organisations/1", json={"name": "Org1", "stability": 1.8})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Org1"
    assert data["stability"] == 1.8


@pytest.mark.asyncio
async def test_delete_organisation_router(client, async_session, seeded_organisations, override_admin_auth):
    response = await client.delete("/api/organisations/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    org_in_db = await async_session.get(Organisation, 1)
    assert org_in_db is None


@pytest_asyncio.fixture
async def seeded_departments(async_session, test_organisation):
    dept = [
        Department(title="it", organisation_id=test_organisation.id),
        Department(title="management", organisation_id=test_organisation.id),
    ]
    async_session.add_all(dept)
    await async_session.commit()
    return dept


@pytest.mark.asyncio
async def test_list_dept_router(client, seeded_departments, override_admin_auth):

    response = await client.get("/api/organisations/departments")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_dept_by_id(client, seeded_departments, override_admin_auth):
    response = await client.get("/api/organisations/departments/1")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "it"


@pytest.mark.asyncio
async def test_create_dept_router(client, async_session, test_organisation, override_admin_auth):
    response = await client.post(
        "/api/organisations/departments", json={"title": "TestDept", "organisation_id": test_organisation.id}
    )

    # Проверки
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "TestDept"
    assert data["organisation_id"] == test_organisation.id


@pytest.mark.asyncio
async def test_update_department_router(client, seeded_departments, override_admin_auth):
    response = await client.patch("/api/organisations/departments/1", json={"title": "TestDept"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "TestDept"


@pytest.mark.asyncio
async def test_delete_department_router(client, async_session, seeded_departments, override_admin_auth):
    response = await client.delete("/api/organisations/departments/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    dept_in_db = await async_session.get(Department, 1)
    assert dept_in_db is None
