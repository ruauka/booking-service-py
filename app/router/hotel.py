from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import HotelAlreadyExistsErr, HotelNotFoundErr, NoHotelsErr, EmptyFieldsToUpdateErr
from app.models.hotel import Hotel
from app.schemas.hotel import HotelRequest, HotelResponse, HotelUpdateRequest
from app.storage.database import get_session
from app.storage.hotel import HotelDAO
from app.utils import set_new_fields

# регистрация роута гостиниц
router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.post("", status_code=201)
async def add_hotel(
        hotel: HotelRequest,
        session: AsyncSession = Depends(get_session),
) -> HotelResponse:
    """
    Создание гостинцы.
    :param hotel: гостиница - входящий JSON
    :param session: async сессия БД
    :return: новая гостиница. http response
    """
    hotel_exist: Hotel = await HotelDAO.get_one(session, name=hotel.name)
    if hotel_exist:
        raise HotelAlreadyExistsErr

    return await HotelDAO.add(session, hotel.dict())


@router.get("/{hotel_id}")
async def get_hotel_by_id(
        hotel_id: int,
        session: AsyncSession = Depends(get_session),
) -> HotelResponse:
    """
    Получение гостиницы по id.
    :param hotel_id: id гостиницы
    :param session: async сессия БД
    :return: гостиница. http response
    """
    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        raise HotelNotFoundErr

    return hotel


@router.get("")
async def get_all_hotels(
        session: AsyncSession = Depends(get_session),
) -> list[HotelResponse]:
    """
    Получение всех гостиниц.
    :param session: async сессия БД
    :return: список гостиниц. http response
    """
    hotels = await HotelDAO.get_all(session)
    if len(hotels) == 0:
        raise NoHotelsErr

    return hotels


@router.put("/{hotel_id}")
async def update_hotel_by_id(
        hotel_id: int,
        new_fields: HotelUpdateRequest,
        session: AsyncSession = Depends(get_session),
) -> HotelResponse:
    """
    Изменение гостиницы по id.
    :param hotel_id: id гостиницы
    :param new_fields: новые поля
    :param session: async сессия БД
    :return: измененная гостиница. http response
    """
    # проверка на полностью пустые поля
    if new_fields.is_empty():
        raise EmptyFieldsToUpdateErr

    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        raise HotelNotFoundErr

    # установка новых значений полей
    updated_fields: dict[str, Any] = set_new_fields(hotel, new_fields)
    return await HotelDAO.update(session, updated_fields, hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotel_by_id(
        hotel_id: int,
        session: AsyncSession = Depends(get_session),
) -> HotelResponse:
    """
    Удаление гостиницы по id.
    :param hotel_id: id гостиницы
    :param session: async сессия БД
    :return: удаленная гостиница. http response
    """
    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        raise HotelNotFoundErr

    return await HotelDAO.delete(session, hotel_id)
