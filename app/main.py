from fastapi import FastAPI
from app.users.router import router as router_users
from app.products.router import router as router_products
from app.carts.router import router as router_carts

app = FastAPI()

app.include_router(router_users)
app.include_router(router_products)
app.include_router(router_carts)
