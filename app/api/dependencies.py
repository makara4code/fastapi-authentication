from uuid import UUID
from app.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from app.models import User
from app.config import settings


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close


SessionDep = Annotated[Session, Depends(get_db)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        user_id_str = payload.get("id")

        if username is None or user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        # Convert to UUID for querying
        try:
            user_id = UUID(user_id_str)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        query = select(User).where(User.id == user_id)
        user = db.scalars(query).first()

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


CurrentUser = Annotated[User, Depends(get_current_user)]
