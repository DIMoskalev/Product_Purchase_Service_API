from httpx import AsyncClient


async def test_add_to_cart(ac: AsyncClient):
    response = await ac.post("/cart/", json={"product_id": 3, "quantity": 3})
    assert response.status_code == 200
    assert response.json() == {"product_id": 3, "quantity": 3}


async def test_add_to_cart_un_active_product(ac: AsyncClient):
    response = await ac.post("/cart/", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 404
    assert response.json()["detail"] == "Товар с текущим id не активен"


async def test_add_to_cart_no_exist_id_product(ac: AsyncClient):
    response = await ac.post("/cart/", json={"product_id": 1000, "quantity": 2})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


async def test_get_cart(ac: AsyncClient):
    response = await ac.get("/cart/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    assert response.json() == {'items': [{'product_id': 3, 'quantity': 3}], 'total_price': 9000}


async def test_add_to_cart_second_product(ac: AsyncClient):
    response = await ac.post("/cart/", json={"product_id": 4, "quantity": 4})
    assert response.status_code == 200
    assert response.json() == {"product_id": 4, "quantity": 4}


async def test_get_updated_cart(ac: AsyncClient):
    response = await ac.get("/cart/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
    assert response.json() == {'items': [{'product_id': 3, 'quantity': 3}, {'product_id': 4, 'quantity': 4}],
                               'total_price': 25000}


async def test_remove_from_cart(ac: AsyncClient):
    response = await ac.delete("/cart/3")
    assert response.status_code == 200
    assert response.json() == {'product_id': 3, 'quantity': 3}


async def test_remove_from_cart_no_id(ac: AsyncClient):
    response = await ac.delete("/cart/1000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart item not found"


async def test_add_to_cart_second_product_again(ac: AsyncClient):
    response = await ac.post("/cart/", json={"product_id": 3, "quantity": 5})
    assert response.status_code == 200
    assert response.json() == {"product_id": 3, "quantity": 5}


async def test_get_updated_cart_again(ac: AsyncClient):
    response = await ac.get("/cart/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
    print(response.json())
    assert response.json() == {'items': [{'product_id': 4, 'quantity': 4}, {'product_id': 3, 'quantity': 5}],
                               'total_price': 31000}


async def test_clear_cart(ac: AsyncClient):
    response = await ac.delete("/cart/clear")
    assert response.status_code == 200
    assert response.json()["detail"] == "Cart cleared"


async def test_get_clear_cart(ac: AsyncClient):
    response = await ac.get("/cart/")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total_price": 0}
