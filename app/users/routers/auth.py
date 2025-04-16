from fastapi import APIRouter, Depends, HTTPException

from app.core.security import create_access_token, verify_password
from app.users import schemas
from app.users.dependencies import get_user_repository
from app.users.repository import UserRepository


router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
async def login(data: schemas.UserLogin, repo: UserRepository = Depends(get_user_repository)):
    user = await repo.get_user_by_email(data.email)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.UserRead)
async def register(
    data: schemas.UserCreate,
    repo: UserRepository = Depends(get_user_repository),
):
    existing = await repo.get_user_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await repo.create_user(data)
    return user
