from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database import engine, Base
from app.users.router import router as router_users
from app.products.router import router as router_products
from app.carts.router import router as router_carts


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Clean up the ML models and release the resources
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(router_users)
app.include_router(router_products)
app.include_router(router_carts)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
