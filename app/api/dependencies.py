from app.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close


SessionDep = Annotated[Session, Depends(get_db)]
