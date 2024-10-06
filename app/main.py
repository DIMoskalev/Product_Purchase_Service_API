from fastapi import FastAPI
from app.database import engine, Base
from app.users.router import router as router_users
from app.products.router import router as router_products

app = FastAPI()


# @app.on_event("startup")
# async def startup():
#     """Событие при запуске приложения для создания таблиц в БД."""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await engine.dispose()


app.include_router(router_users)
app.include_router(router_products)
# app.include_router(cart.router, prefix="/cart", tags=["cart"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
