from fastapi import APIRouter, Depends, Path, status

from app.organisation import schemas
from app.organisation.dependencies import get_department_repository, get_organisation_repository
from app.organisation.repository import DepartmentRepository, OrganisationRepository


router = APIRouter(prefix="/api/organisations", tags=["Organisations"])


@router.get("/", response_model=list[schemas.OrganisationRead])
async def list_organisations(repo: OrganisationRepository = Depends(get_organisation_repository)):
    return await repo.get_all()


@router.get("/{org_id}", response_model=schemas.OrganisationRead)
async def get_organisation(
    org_id: int = Path(..., gt=0), repo: OrganisationRepository = Depends(get_organisation_repository)
):
    return await repo.get_by_id(org_id)


@router.post("/", response_model=schemas.OrganisationRead, status_code=status.HTTP_201_CREATED)
async def create_organisation(
    organisation: schemas.OrganisationCreate, repo: OrganisationRepository = Depends(get_organisation_repository)
):
    return await repo.create(organisation)


@router.patch("/{org_id}", response_model=schemas.OrganisationRead, status_code=status.HTTP_200_OK)
async def update_stability(
    org_id: int = Path(..., gt=0),
    org_in: schemas.OrganisationUpdate = ...,
    repo: OrganisationRepository = Depends(get_organisation_repository),
):
    return repo.update(org_id, org_in)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organisation(org_id: int, repo: OrganisationRepository = Depends(get_organisation_repository)):
    await repo.delete(org_id)


@router.get("/departments", response_model=list[schemas.DepartmentRead])
async def list_departments(repo: DepartmentRepository = Depends(get_department_repository)):
    return await repo.get_all()


@router.get("/departments/{department_id}", response_model=schemas.DepartmentRead)
async def get_department(
    department_id: int = Path(..., gt=0), repo: DepartmentRepository = Depends(get_department_repository)
):
    return await repo.get_by_id(department_id)


@router.post("/departments", response_model=schemas.DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(
    department: schemas.DepartmentCreate, repo: DepartmentRepository = Depends(get_department_repository)
):
    return await repo.create(department)


@router.patch("/departments/{department_id}", response_model=schemas.DepartmentRead, status_code=status.HTTP_200_OK)
async def update_department(
    dept_id: int = Path(..., gt=0),
    dept_in: schemas.DepartmentUpdate = ...,
    repo: DepartmentRepository = Depends(get_department_repository),
):
    return await repo.update(dept_id, dept_in)


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(dept_id: int, repo: DepartmentRepository = Depends(get_department_repository)):
    await repo.delete(dept_id)
