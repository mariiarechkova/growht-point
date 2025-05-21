from fastapi import APIRouter, Depends, Path

from app.users import schemas
from app.users.dependencies import get_user_service, require_admin_user
from app.users.models import User
from app.users.services.user_services import UserService


router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserRead])
async def list_users(
    current_user: User = Depends(require_admin_user), service: UserService = Depends(get_user_service)
):
    return await service.get_all_users(current_user.organisation_id)


@router.get("/{user_id}", response_model=schemas.UserRead)
async def get_user(user_id: int = Path(..., gt=0), service: UserService = Depends(get_user_service)):
    return await service.get_user_by_id(user_id)
