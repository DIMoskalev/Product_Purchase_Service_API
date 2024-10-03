from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, products, cart


app = FastAPI()


@app.on_event("startup")
async def startup():
    """Событие при запуске приложения для создания таблиц в БД."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(products.router, prefix="/products", tags=["products"])
# app.include_router(cart.router, prefix="/cart", tags=["cart"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)