from fastapi import FastAPI

from app.api.main import api_router
from app.models import Base
from app.database import engine
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)
Base.metadata.create_all(bind=engine)
