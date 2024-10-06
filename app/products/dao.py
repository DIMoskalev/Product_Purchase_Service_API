from app.dao.base import BaseDAO
from app.models import Product


class ProductsDAO(BaseDAO):
    model = Product
