import pytest_asyncio

from app.organisation.models import Organisation


@pytest_asyncio.fixture
async def test_organisation(async_session):
    org = Organisation(name="TestOrg")
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)
    return org
