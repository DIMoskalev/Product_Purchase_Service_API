from httpx import AsyncClient


async def test_create_product_admin(ac: AsyncClient):
    data = {
        "name": "Test Product",
        "description": "Test Product Description",
        "price": 2000,
        "quantity": 5,
    }
    response = await ac.post("/products/create_product/", json=data)
    assert response.status_code == 200


async def test_create_the_same_product_admin(ac: AsyncClient):
    data = {
        "name": "Test Product",
        "description": "Test Product Description",
        "price": 2000,
        "quantity": 5,
    }
    response = await ac.post("/products/create_product/", json=data)
    assert response.status_code == 409


async def test_update_product_admin(ac: AsyncClient):
    data = {
        "name": "Test Product Updated",
        "description": "Test Product Description Updated",
        "price": 2500,
        "quantity": 10,
        "is_active": False,
    }
    response = await ac.put("/products/1/", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product Updated"


async def test_create_second_product_admin(ac: AsyncClient):
    data = {
        "name": "Test Product 2",
        "description": "Test Product Description 2",
        "price": 3000,
        "quantity": 10,
    }
    response = await ac.post("/products/create_product/", json=data)
    assert response.status_code == 200


async def test_get_active_products(ac: AsyncClient):
    response = await ac.get("/products/active_products/")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_products_admin(ac: AsyncClient):
    response = await ac.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_product_delete_admin(ac: AsyncClient):
    response = await ac.delete("/products/2/")
    assert response.status_code == 200


async def test_get_all_products_after_delete_admin(ac: AsyncClient):
    response = await ac.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_active_products_after_delete(ac: AsyncClient):
    response = await ac.get("/products/active_products/")
    assert response.status_code == 404
    print(response.json())
    assert response.json() == {'detail': 'Не найдены активные товары'}


async def test_get_non_existent_product(ac: AsyncClient):
    response = await ac.get("/products/3/")
    assert response.status_code == 404


async def test_create_product_again_admin(ac: AsyncClient):
    data = {
        "name": "Test Product",
        "description": "Test Product Description",
        "price": 2000,
        "quantity": 5,
    }
    response = await ac.post("/products/create_product/", json=data)
    assert response.status_code == 200


async def test_get_product_info(ac: AsyncClient):
    response = await ac.get("/products/3/")
    assert response.status_code == 200
    print(response.json())
    assert response.json()[0] == {'name': 'Test Product', 'price': 2000, 'id': 3, 'is_active': True}


async def test_update_product_non_existent(ac: AsyncClient):
    data = {
        "name": "Test Product Updated",
        "description": "Test Product Description Updated",
        "price": 2500,
        "quantity": 10,
        "is_active": False,
    }
    response = await ac.put("/products/1000/", json=data)
    assert response.status_code == 404


async def test_delete_product_non_existent(ac: AsyncClient):
    response = await ac.delete("/products/1000/")
    assert response.status_code == 404


async def test_logout_admin(ac: AsyncClient):
    response = await ac.post("/users/logout/")
    assert response.status_code == 200


async def test_login_not_admin(ac: AsyncClient):
    response = await ac.post("/users/login/", json={
        "full_name": "Test",
        "email": "Test@test.ru",
        "phone": "+79999999999",
        "hashed_password": "Testtesttest!"
    }
                             )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_create_product__not_admin(ac: AsyncClient):
    data = {
        "name": "Test Product false",
        "description": "Test Product Description",
        "price": 2000,
        "quantity": 5,
    }
    response = await ac.post("/products/create_product/", json=data)
    assert response.status_code == 403


async def test_update_product_not_admin(ac: AsyncClient):
    data = {
        "name": "Test Product Updated",
        "description": "Test Product Description Updated",
        "price": 2500,
        "quantity": 10,
        "is_active": False,
    }
    response = await ac.put("/products/1/", json=data)
    assert response.status_code == 403


async def test_get_all_products_no_admin(ac: AsyncClient):
    response = await ac.get("/products/")
    assert response.status_code == 403


async def test_product_delete_not_admin(ac: AsyncClient):
    response = await ac.delete("/products/2/")
    assert response.status_code == 403
