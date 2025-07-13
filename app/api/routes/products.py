from fastapi import APIRouter
from app.api.dependencies import CurrentUser, SessionDep

router = APIRouter(prefix="/products", tags=["products"])


# GET: /products/
@router.get("/")
async def read_all_product(db: SessionDep, current_user: CurrentUser):
    return {"data": "read all product"}




# POST /products/
@router.post("/")
async def create_new_proudct(db: SessionDep, current_user: CurrentUser):
    return {"data": "create new product"}
