from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import SessionDep
from app.models import User
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from app.services.auth import bcrypt_context, authenticate, create_access_token
from app.schemas import Token, CreateUserRequest
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

# FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
# FormDep = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]


# /auth/login
@router.post("/token", response_model=Token)
async def login(db: SessionDep, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate(db, form.username, form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(
        user.username, user.id, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": token, "token_type": "bearer"}


# /auth/register
@router.post("/register", status_code=201)
async def register(db: SessionDep, create_user_request: CreateUserRequest):
    # uv add "passlib[bcrypt]"
    # uv add python-jose[cryptography]
    # uv add bcrypt==4.0.1
    hashed_password = bcrypt_context.hash(create_user_request.passowrd)

    create_user_model = User(
        username=create_user_request.username, password=hashed_password
    )

    db.add(create_user_model)
    db.commit()
