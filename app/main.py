from fastapi import FastAPI

from app.organisation.router import router as organisation_router
from app.users.routers import router as user_router


app = FastAPI()

app.include_router(organisation_router)
app.include_router(user_router)
