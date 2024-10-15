from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, str_uniq, str_null_false, bool_default_false, int_null_false, bool_default_true


# Создаем модель таблицы пользователей
class User(Base):
    full_name: Mapped[str]
    email: Mapped[str_uniq]
    phone: Mapped[str_uniq]
    hashed_password: Mapped[str_null_false]
    is_active: Mapped[bool_default_true]
    is_admin: Mapped[bool_default_false]

    carts: Mapped["Cart"] = relationship("Cart", back_populates="users")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"fullname={self.full_name!r},"
                f"email={self.email!r})")

    def __repr__(self):
        return str(self)


# Создаем модель таблицы товаров
class Product(Base):
    name: Mapped[str_null_false]
    price: Mapped[int_null_false]
    is_active: Mapped[bool_default_true]

    cartitems: Mapped["CartItem"] = relationship("CartItem", back_populates="products", lazy="selectin")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, price={self.price})"

    def __repr__(self):
        return str(self)


# Создаем модель таблицы корзины
class Cart(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    users: Mapped["User"] = relationship("User", back_populates="carts", lazy="selectin")
    cartitems: Mapped["CartItem"] = relationship("CartItem", back_populates="carts", lazy="selectin")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)


class CartItem(Base):

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int_null_false] = mapped_column(default=1)

    carts: Mapped["Cart"] = relationship("Cart", back_populates="cartitems", lazy="selectin")
    products: Mapped["Product"] = relationship("Product", back_populates="cartitems", lazy="selectin")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})"

    def __repr__(self):
        return str(self)
