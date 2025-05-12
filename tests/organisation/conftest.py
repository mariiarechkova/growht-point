import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_session
from app.main import app
from app.organisation.models import Organisation


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def test_organisation(async_session):
    org = Organisation(name="TestOrg")
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)
    return org


@pytest_asyncio.fixture
async def client(async_session):
    # Переопределяем Depends(get_session)
    app.dependency_overrides[get_session] = lambda: async_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
