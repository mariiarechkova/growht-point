from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.organisation import schemas
from app.organisation.dependencies import get_department_repository, get_organisation_repository
from app.organisation.repository import DepartmentRepository, OrganisationRepository
from app.organisation.schemas import OrganisationAndUserCreate
from app.organisation.services.organisation_user_create import OrganisationUserCreatorService
from app.users.dependencies import require_admin_user


router = APIRouter(prefix="/api/organisations", tags=["Organisations"])


@router.get("/", response_model=list[schemas.OrganisationRead])
async def list_organisations(repo: OrganisationRepository = Depends(get_organisation_repository)):
    return await repo.get_all()


@router.get("/{org_id}", response_model=schemas.OrganisationRead)
async def get_organisation(
    org_id: int = Path(..., gt=0), repo: OrganisationRepository = Depends(get_organisation_repository)
):
    return await repo.get_by_id(org_id)


@router.post("/", response_model=schemas.OrganisationWithUser, status_code=status.HTTP_201_CREATED)
async def create_organisation_with_user(
    data: OrganisationAndUserCreate,
    session: AsyncSession = Depends(get_session),
):
    service = OrganisationUserCreatorService(session)
    organisation, user = await service.create(data)

    return {"organisation": organisation, "user": user}


@router.patch(
    "/{org_id}",
    response_model=schemas.OrganisationRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin_user)],
)
async def update_stability(
    org_id: int = Path(..., gt=0),
    org_in: schemas.OrganisationUpdate = ...,
    repo: OrganisationRepository = Depends(get_organisation_repository),
):
    return repo.update(org_id, org_in)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin_user)])
async def delete_organisation(org_id: int, repo: OrganisationRepository = Depends(get_organisation_repository)):
    await repo.delete(org_id)


@router.get("/departments", response_model=list[schemas.DepartmentRead], dependencies=[Depends(require_admin_user)])
async def list_departments(repo: DepartmentRepository = Depends(get_department_repository)):
    return await repo.get_all()


@router.get(
    "/departments/{department_id}", response_model=schemas.DepartmentRead, dependencies=[Depends(require_admin_user)]
)
async def get_department(
    department_id: int = Path(..., gt=0), repo: DepartmentRepository = Depends(get_department_repository)
):
    return await repo.get_by_id(department_id)


@router.post(
    "/departments",
    response_model=schemas.DepartmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_user)],
)
async def create_department(
    department: schemas.DepartmentCreate, repo: DepartmentRepository = Depends(get_department_repository)
):
    return await repo.create(department)


@router.patch(
    "/departments/{department_id}",
    response_model=schemas.DepartmentRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin_user)],
)
async def update_department(
    dept_id: int = Path(..., gt=0),
    dept_in: schemas.DepartmentUpdate = ...,
    repo: DepartmentRepository = Depends(get_department_repository),
):
    return await repo.update(dept_id, dept_in)


@router.delete(
    "/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin_user)]
)
async def delete_department(dept_id: int, repo: DepartmentRepository = Depends(get_department_repository)):
    await repo.delete(dept_id)
