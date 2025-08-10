from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateUserRequest(BaseModel):
    username: str
    passowrd: str


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ProductResponse(ProductBase):
    id: UUID

    class Config:
        from_attributes = True
