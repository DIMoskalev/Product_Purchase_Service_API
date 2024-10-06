from typing import List

from pydantic import BaseModel


class CartItemResponse(BaseModel):
    product_id: int
    quantity: int


class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_price: int


class CartCreate(BaseModel):
    product_id: int
    quantity: int
