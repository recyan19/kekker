""" Tests for Users API """
import jwt
from fastapi.testclient import TestClient

from app import schemas
from app.config import settings


def test_create_user(client: TestClient):
    """ Test user creation """
    response = client.post("/users/", json={"email": "yan1@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "yan1@gmail.com"
    assert response.status_code == 201


def test_login_user(client: TestClient, test_user):  # type: ignore
    """ Test login user """
    data: dict[str, str] = {"username": test_user["email"], "password": test_user["password"]}
    response = client.post("/login/", data=data)
    login_res = schemas.Token(**response.json())

    payload = jwt.decode(
        login_res.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm]
        )
    user_id = int(payload.get("user_id"))

    assert user_id == test_user["id"]
    assert login_res.token_type == 'bearer'
    assert response.status_code == 200
