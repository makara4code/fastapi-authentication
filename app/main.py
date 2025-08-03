from fastapi import FastAPI

from app.api.main import api_router
from app.models import Base
from app.database import engine
from app.config import settings

app = FastAPI()
print("Here is envs:", settings.model_dump())

app.include_router(api_router)
Base.metadata.create_all(bind=engine)
