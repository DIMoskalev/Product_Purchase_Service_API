from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal, get_db
from app.exceptions import ForbiddenException, ProductAlreadyExistsException, NoProductIdException, \
    NoActiveProductException
from app.models import Product, User

from app.products.dao import ProductsDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.products.schemas import ProductGet, ProductCreate, ProductUpdate, ProductDelete

router = APIRouter(prefix="/products", tags=["Работа с товарами"])


@router.get("/", summary="Получить все товары", response_model=list[ProductGet])
async def get_all_products(user_data: User = Depends(get_current_admin_user)):
    return await ProductsDAO.get_all()


@router.get("/active_products/", summary="Получить все активные товары", response_model=list[ProductGet])
async def get_active_products(user_data: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.is_active == True))
    products = result.scalars().all()  # Получение списка всех активных товаров

    if not products:
        raise NoActiveProductException

    return products


@router.get("/{product_id}/", summary="Получить информацию о текущем товаре", response_model=list[ProductGet])
async def get_product_info(product_id: int, user_data: User = Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    products = result.scalars().all()  # Получение списка из одного, запрошенного товара

    if not products:
        raise NoProductIdException

    return products


@router.post("/create_product/", summary="Создать товар")
async def create_product(product_data: ProductCreate, user: User = Depends(get_current_admin_user)):
    product = await ProductsDAO.get_one_or_none(name=product_data.name)
    if product:
        raise ProductAlreadyExistsException
    # Только для администраторов
    if not user.is_admin:
        raise ForbiddenException
    product_dict = product_data.model_dump()
    await ProductsDAO.add(**product_dict)
    return {'message': f'Вы успешно добавили товар!'}


@router.put("/{product_id}/", summary="Обновить информацию о товаре", response_model=ProductUpdate)
async def update_product(product_id: int, updated_product: ProductUpdate, user: User = Depends(get_current_admin_user),
                         db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()  # Получаем товар или None

        if product is None:
            raise NoProductIdException

        if not user.is_admin:
            raise ForbiddenException

        # Обновляем поля товара
        product.name = updated_product.name
        product.price = updated_product.price
        product.is_active = updated_product.is_active

        await db.commit()  # Сохраняем изменения

    return product  # Возвращаем обновленный товар


@router.delete("/{product_id}/", summary="Удалить товар", response_model=dict)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_admin_user)):
    # Ищем товар по ID
    result = await session.execute(select(Product).filter(Product.id == product_id))
    product = result.scalar_one_or_none()

    if product is None:
        raise NoProductIdException

    if not user.is_admin:
        raise ForbiddenException

    # Удаляем товар
    await session.delete(product)
    await session.commit()

    return {"message": "Товар успешно удален!"}
