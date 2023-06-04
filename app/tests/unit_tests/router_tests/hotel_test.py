import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("name, location, services, rooms_quantity, image_id, status_code", [
    ("test_name", "test_location", ["test_services1", "test_services2"], 10, 100, 201),
    ("test_name", "test_location", ["test_services1", "test_services2"], 10, 100, 400),
])
async def test_add_hotel(
        admin_async_client: AsyncClient,
        name,
        location,
        services,
        rooms_quantity,
        image_id,
        status_code
):
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


async def test_get_all_hotels(async_client: AsyncClient):
    """Тест получения всех гостиниц"""
    resp = await async_client.get(f"/hotels")
    assert resp.status_code == 200


@pytest.mark.parametrize("hotel_id, name, location, services, rooms_quantity, image_id, status_code", [
    (6, "test_name2", "test_location2", ["test_services1", "test_services2"], 6, 6, 200),
    (3, "test_name2", "test_location2", ["test_services1", "test_services2"], 2, 2, 400),
    (2, None, None, None, None, None, 400),
    (100, "test_name", "test_location", ["test_services1", "test_services1"], 2, 2, 400),
])
async def test_update_hotel_by_id(
        admin_async_client: AsyncClient,
        hotel_id,
        name,
        location,
        services,
        rooms_quantity,
        image_id,
        status_code
):
    """Тест обновления гостиницы"""
    resp = await admin_async_client.put(f"/hotels/{hotel_id}", json={
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
async def test_delete_hotel_by_id(admin_async_client: AsyncClient, hotel_id, status_code):
    """Тест удаления гостиницы по id"""
    resp = await admin_async_client.delete(f"/hotels/{hotel_id}")
    assert resp.status_code == status_code
