from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# 1. Создаём асинхронный движок PostgreSQL
engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)

# 2. Создаём фабрику сессий (чтобы делать запросы к БД)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


# 3. Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
