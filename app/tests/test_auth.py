from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register():
    response = client.post("/users/register", json={
        "full_name": "Test",
        "email": "Test@test.tu",
        "phone": "+79999999999",
        "hashed_password": "Testtesttest!"
    }
                           )

    assert response.status_code == 200
