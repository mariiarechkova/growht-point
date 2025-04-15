from fastapi import APIRouter, Depends, Path

from app.users import schemas
from app.users.dependencies import get_user_repository
from app.users.repository import UserRepository


router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserRead])
async def list_users(repo: UserRepository = Depends(get_user_repository)):
    return await repo.get_all()


@router.get("/{user_id}", response_model=schemas.UserRead)
async def get_user(user_id: int = Path(..., gt=0), repo: UserRepository = Depends(get_user_repository)):
    return await repo.get_user_by_id(user_id)
