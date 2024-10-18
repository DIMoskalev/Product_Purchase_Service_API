from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.exceptions import ProductIsUnActive
from app.models import Cart, CartItem, Product, User
from app.carts.schemas import CartCreate, CartItemResponse, CartResponse
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Работа с корзиной"])


@router.post("/", response_model=CartItemResponse, summary="Добавить товар в корзину")
async def add_to_cart(cartitems: CartCreate, user_data: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    """Добавление товара в корзину."""
    user_result = await db.execute(select(User).filter(User.id == user_data.id))
    user = user_result.scalars().first()

    product_result = await db.execute(select(Product).filter(Product.id == cartitems.product_id))
    product = product_result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.is_active is False:
        raise ProductIsUnActive

    cart = await db.execute(select(Cart).filter(Cart.user_id == user.id))
    cart = cart.scalars().first()

    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        await db.commit()

    cart_item = await db.execute(
        select(CartItem).filter(CartItem.product_id == product.id, CartItem.cart_id == cart.id))
    cart_item = cart_item.scalars().first()
    if cart_item:
        cart_item.quantity += cartitems.quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=cartitems.quantity)
        db.add(cart_item)

    await db.commit()
    await db.refresh(cart_item)

    return cart_item


@router.get("/", response_model=CartResponse, summary="Посмотреть содержимое корзины")
async def get_cart(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Получение содержимого корзины текущего пользователя."""
    user_result = await db.execute(select(User).filter(User.id == user.id))
    user = user_result.scalars().first()

    cart_result = await db.execute(select(Cart).filter(Cart.user_id == user.id))
    cart = cart_result.scalars().first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items_result = await db.execute(select(CartItem).filter(CartItem.cart_id == cart.id))
    items = items_result.scalars().all()
    total_price = sum(item.products.price * item.quantity for item in items)

    return {"items": [{"product_id": item.product_id, "quantity": item.quantity} for item in items],
            "total_price": total_price}


@router.delete("/clear", response_model=dict, summary="Удалить все товары из корзины")
async def clear_cart(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Очистка корзины текущего пользователя."""
    user_result = await db.execute(select(User).filter(User.id == user.id))
    user = user_result.scalars().first()

    cart_result = await db.execute(select(Cart).filter(Cart.user_id == user.id))
    cart = cart_result.scalars().first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item_result = await db.execute(select(CartItem).filter(CartItem.cart_id == cart.id))
    cart_items = cart_item_result.scalars().all()

    for cart_item in cart_items:
        await db.delete(cart_item)

    await db.commit()

    return {"detail": "Cart cleared"}


@router.delete("/{product_id}", response_model=CartItemResponse, summary="Удалить товар из корзины")
async def remove_from_cart(product_id: int, user_data: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    """Удаление товара из корзины по ID."""
    user_result = await db.execute(select(User).filter(User.id == user_data.id))
    user = user_result.scalars().first()

    cart_result = await db.execute(select(Cart).filter(Cart.user_id == user.id))
    cart = cart_result.scalars().first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item_result = await db.execute(
        select(CartItem).filter(CartItem.product_id == product_id, CartItem.cart_id == cart.id))
    cart_item = cart_item_result.scalars().first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await db.delete(cart_item)
    await db.commit()

    return cart_item
