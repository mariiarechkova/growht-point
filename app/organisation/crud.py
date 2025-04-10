from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.organisation import models, schemas


async def create_organisation(session: AsyncSession, org_in: schemas.OrganisationCreate) -> models.Organisation:
    org = models.Organisation(
        **org_in.dict()
    )  # превращаем Pydantic-модель в обычный словарь и передаём в SQLAlchemy-модель
    session.add(org)  # добавляем объект в сессию. Это ещё не вставка в БД
    await session.commit()  # выполняем SQL-запрос INSERT INTO organisations
    await session.refresh(org)  # загружаем авто-сгенерированные поля (например, id, created_at) обратно в объект.
    return org  # возвращаем SQLAlchemy-модель, которую FastAPI потом преобразует в JSON через response_model


async def get_all_organisations(session: AsyncSession) -> list[models.Organisation]:
    result = await session.execute(select(models.Organisation))  # создаёт SQL-запрос SELECT * FROM organisations,
    # выполняет запрос и возвращает "сырой" результат
    return result.scalars().all()  # извлекает все строки, как список объектов Organisation


async def update_organisation_stability(
    session: AsyncSession, org_id: int, org_in: schemas.OrganisationUpdate
) -> models.Organisation:
    result = await session.execute(select(models.Organisation).where(models.Organisation.id == org_id))
    organisation = result.scalar_one_or_none()

    if organisation is None:
        raise HTTPException(status_code=404, detail="Organisation not found")

    organisation.stability = org_in.stability
    await session.commit()
    await session.refresh(organisation)
    return organisation
