from fastapi import FastAPI

from app.organisation.router import router as organisation_router
from app.users.routers import routers as user_routers
from app.voting.routers import router as voting_routers


app = FastAPI()

app.include_router(organisation_router)
app.include_router(voting_routers)

for router in user_routers:
    app.include_router(router)
