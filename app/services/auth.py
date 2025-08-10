from datetime import timedelta, timezone, datetime
from jose import jwt
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import User
from passlib.context import CryptContext
from app.config import settings

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    # store UUID as string in token payload for portability
    payload = {"sub": username, "id": str(user_id)}
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expires})

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def authenticate(db: Session, username: str, password: str):
    query = select(User).where(User.username == username)
    user = db.scalars(query).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.password):
        return False

    return user
