from fastapi import APIRouter
from app.api.dependencies import SessionDep
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import SessionDep
from pydantic import BaseModel
from app.models import User
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# /auth/login
@router.post("/login")
async def login(db: SessionDep):
    # username: admin, password: 123

    return {"data": "login"}


class CreateUserRequest(BaseModel):
    username: str
    passowrd: str


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
