from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.organisation import crud, schemas


router = APIRouter(prefix="/api/organisations", tags=["Organisations"])


@router.post("/", response_model=schemas.OrganisationRead, status_code=201)
async def create_organisation(
    organisation: schemas.OrganisationCreate,
    session: AsyncSession = Depends(get_session),
):
    return await crud.create_organisation(session, organisation)


@router.get("/", response_model=list[schemas.OrganisationRead])
async def list_organisations(session: AsyncSession = Depends(get_session)):
    return await crud.get_all_organisations(session)


@router.patch("/{org_id}", response_model=schemas.OrganisationRead, status_code=200)
async def update_stability(
    org_id: int = Path(..., gt=0),
    org_in: schemas.OrganisationUpdate = ...,
    session: AsyncSession = Depends(get_session),
):
    return await crud.update_organisation_stability(session, org_id, org_in)
