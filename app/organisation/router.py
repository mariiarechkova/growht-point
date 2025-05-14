from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.organisation import schemas
from app.organisation.dependencies import get_department_service, get_organisation_service
from app.organisation.schemas import OrganisationAndUserCreate
from app.organisation.services.common_services import DepartmentService, OrganisationService
from app.organisation.services.organisation_user_create import OrganisationUserCreatorService
from app.users.dependencies import require_admin_user


router = APIRouter(prefix="/api/organisations", tags=["Organisations"])


@router.get("/", response_model=list[schemas.OrganisationRead])
async def list_organisations(
    order_by: str = Query("created_at", enum=["name", "created_at"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    service: OrganisationService = Depends(get_organisation_service),
):
    return await service.get_all(order_by, order)


@router.get("/departments", response_model=list[schemas.DepartmentRead], dependencies=[Depends(require_admin_user)])
async def list_departments(service: DepartmentService = Depends(get_department_service)):
    return await service.get_all()


@router.get("/{org_id}", response_model=schemas.OrganisationRead)
async def get_organisation(
    org_id: int = Path(..., gt=0), service: OrganisationService = Depends(get_organisation_service)
):
    return await service.get_by_id(org_id)


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
    service: OrganisationService = Depends(get_organisation_service),
):
    return await service.update(org_id, org_in)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin_user)])
async def delete_organisation(org_id: int, service: OrganisationService = Depends(get_organisation_service)):
    await service.delete(org_id)


@router.get(
    "/departments/{department_id}", response_model=schemas.DepartmentRead, dependencies=[Depends(require_admin_user)]
)
async def get_department(
    department_id: int = Path(..., gt=0), service: DepartmentService = Depends(get_department_service)
):
    return await service.get_by_id(department_id)


@router.post(
    "/departments",
    response_model=schemas.DepartmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_user)],
)
async def create_department(
    department: schemas.DepartmentCreate, service: DepartmentService = Depends(get_department_service)
):
    return await service.create(department)


@router.patch(
    "/departments/{dept_id}",
    response_model=schemas.DepartmentRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin_user)],
)
async def update_department(
    dept_id: int = Path(..., gt=0),
    dept_in: schemas.DepartmentUpdate = ...,
    service: DepartmentService = Depends(get_department_service),
):
    return await service.update(dept_id, dept_in)


@router.delete(
    "/departments/{dept_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin_user)]
)
async def delete_department(dept_id: int, service: DepartmentService = Depends(get_department_service)):
    await service.delete(dept_id)
