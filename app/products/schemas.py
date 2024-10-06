from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    is_active: bool


class ProductDelete(BaseModel):
    name: str


class ProductGet(ProductBase):
    id: int
    is_active: bool
