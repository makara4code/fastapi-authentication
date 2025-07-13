from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


# GET: /products/
@router.get("/")
async def read_all_product():
    return {"data": "read all product"}


# POST /products/
@router.post("/")
async def create_new_proudct():
    return {"data": "create new product"}
