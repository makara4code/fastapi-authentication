from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


# GET: /users/
@router.get("/")
async def list_users():
    return {"data": "read all users"}


# POST /users/
@router.post("/")
async def create_new_user():
    return {"data": "create new user"}
