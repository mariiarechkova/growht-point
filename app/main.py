from fastapi import FastAPI

from app.organisation.router import router as organisation_router
from app.users.routers import routers as user_routers


app = FastAPI()

app.include_router(organisation_router)

for router in user_routers:
    app.include_router(router)
