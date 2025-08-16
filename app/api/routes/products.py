from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser, SessionDep
from app.models import Product
from app.schemas import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


# GET: /products/
@router.get("/", response_model=List[ProductResponse])
async def list_products(db: SessionDep, current_user: CurrentUser):
    query = select(Product).where(Product.user_id == current_user.id)
    products = db.scalars(query).all()
    return products


# POST /products/
@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    payload: ProductCreate,
    db: SessionDep,
    current_user: CurrentUser,
):
    product = Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        user_id=current_user.id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def _get_owned_product_or_404(db: Session, user_id: int, product_id: UUID) -> Product:
    product = db.get(Product, product_id)
    if not product or product.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


# GET /products/{product_id}
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    db: SessionDep,
    current_user: CurrentUser,
):
    product = _get_owned_product_or_404(db, current_user.id, product_id)
    return product


# PUT /products/{product_id}
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    db: SessionDep,
    current_user: CurrentUser,
):
    product = _get_owned_product_or_404(db, current_user.id, product_id)

    # if payload.name is not None:
    #     product.name = payload.name
    # if payload.description is not None:
    #     product.description = payload.description
    # if payload.price is not None:
    #     product.price = payload.price

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# DELETE /products/{product_id}
@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: UUID,
    db: SessionDep,
    current_user: CurrentUser,
):
    product = _get_owned_product_or_404(db, current_user.id, product_id)
    db.delete(product)
    db.commit()
    return None
