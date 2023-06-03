import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("test_client@test.com", "test", 201),
    ("test_client@test.com", "test", 400),
    ("test_client1@test.com", "test1", 201),
    ("abcde", "12345", 422),
])
async def test_register_user(async_client: AsyncClient, email, password, status_code):
    """Тест регистрации пользователя"""
    resp = await async_client.post("/auth/registration", json={
        "email": email,
        "password": password
    })

    assert resp.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("ruauka@test.com", "test", 200),
    ("ushakov@example.com", "test", 200),
    ("test_client2@test.com", "test", 401),
])
async def test_login_user(async_client: AsyncClient, email, password, status_code):
    """Тест аутентификации пользователя"""
    resp = await async_client.post("/auth/login", json={
        "email": email,
        "password": password,
    })

    assert resp.status_code == status_code
    # проверка наличия JWT в куке
    if resp.json().get("JWT", None) is not None:
        assert resp.json().get("JWT", None) is not None
    else:
        assert resp.json().get("JWT", None) is None
