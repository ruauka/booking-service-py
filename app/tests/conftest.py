import pytest
import asyncio
import json
from datetime import datetime
from httpx import AsyncClient
from sqlalchemy import insert

from app.storage.database import Base, async_session_maker, engine, get_session
from app.models.user import User
from app.models.room import Room
from app.models.hotel import Hotel
from app.models.booking import Booking
from main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """
    Фикстура создания таблиц и наполнения их данными в тестовой БД.
    autouse=True - вызов фикстуры перед запуском первого теста.
    scope="session" - вызов фикстуры 1 раз на время прогона всех тестов.
    """
    async with engine.begin() as conn:
        # Удаление всех таблиц из БД
        await conn.run_sync(Base.metadata.drop_all)
        # Добавление всех таблиц в БД
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_jsons/{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        # конвертация строковой даты в формат datetime для SQLAlchemy
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Hotel, hotels),
            (Room, rooms),
            (User, users),
            (Booking, bookings),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="function")
async def async_client():
    """
    Фикстура создания асинхронного клиента для тестирования эндпоинтов.
    Чистый клиент, без кук.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="function")
async def auth_async_client():
    """
    Фикстура создания асинхронного аутентифицированного клиента для тестирования эндпоинтов.
    Содержит JWT в куке.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as auth_async_client:
        await auth_async_client.post("/auth/login", json={
            "email": "ruauka@test.com",
            "password": "test",
        })
        assert auth_async_client.cookies["JWT"]
        yield auth_async_client


# @pytest.fixture(scope="function")
# async def session():
#     async with async_session_maker() as session:
#         yield session


@pytest.fixture(scope="session")
def event_loop(request):
    """
    Взято из доки pytest-asyncio.
    Create an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
