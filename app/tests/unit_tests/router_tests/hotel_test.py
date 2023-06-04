import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("name, location, services, rooms_quantity, image_id, status_code", [
    ("test_name", "test_location", ["test_services1", "test_services1"], 10, 100, 201),
    ("test_name", "test_location", ["test_services1", "test_services1"], 10, 100, 400),
])
async def test_add_hotel(admin_async_client: AsyncClient, name, location, services, rooms_quantity, image_id,
                         status_code):
    """Тест добавления гостиницы"""
    resp = await admin_async_client.post("/hotels", json={
        "name": name,
        "location": location,
        "services": services,
        "rooms_quantity": rooms_quantity,
        "image_id": image_id
    })

    assert resp.status_code == status_code


@pytest.mark.parametrize("hotel_id, status_code", [
    (1, 200),
    (100, 400),
])
async def test_get_hotel_by_id(admin_async_client: AsyncClient, hotel_id, status_code):
    """Тест получения гостиницы по id"""
    resp = await admin_async_client.get(f"/hotels/{hotel_id}")
    assert resp.status_code == status_code
