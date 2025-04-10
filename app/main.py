from fastapi import FastAPI

from app.organisation.router import router as organisation_router


app = FastAPI()

app.include_router(organisation_router)
