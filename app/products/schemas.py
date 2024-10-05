from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: int


class ProductUpdate(BaseModel):
    name: str
    price: int
    is_active: bool


class ProductGet(BaseModel):
    id: int
    name: str
    price: float
    is_active: bool

