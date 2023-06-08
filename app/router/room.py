from datetime import date, datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import admin_check
from app.errors import (
    EmptyFieldsToUpdateErr,
    HotelNotFoundErr,
    NoRoomsErr,
    NoRoomsOnPeriodErr,
    RoomAlreadyExistsErr,
    RoomNotFoundErr,
)
from app.logger import logger
from app.models.room import Room
from app.schemas.room import RoomRequest, RoomResponse, RoomUpdateRequest
from app.storage.database import get_session
from app.storage.hotel import HotelDAO
from app.storage.room import RoomDAO
from app.utils import set_new_fields

# регистрация роута комнат
router = APIRouter(
    prefix="/hotels",
    tags=["Rooms"],
)


@router.get("/{hotel_id}/rooms/free")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
        session: AsyncSession = Depends(get_session),
) -> List[RoomResponse]:
    """
    Получение списока всех свободных для бронирования номеров определенной гостиницы.
    :param hotel_id: id гостиницы
    :param date_from: дата бронирования 'с'
    :param date_to: дата бронирования 'по'
    :param session: session: async сессия БД
    :return: список номеров
    """
    rooms = await RoomDAO.get_rooms_by_time(session, hotel_id, date_from, date_to)
    if len(rooms) == 0:
        logger.error(NoRoomsOnPeriodErr.detail, extra={"status_code": NoRoomsOnPeriodErr.status_code})
        raise NoRoomsOnPeriodErr

    return rooms


@router.post("/{hotel_id}/rooms", dependencies=[Depends(admin_check)], status_code=201)
async def add_room(
        hotel_id: int,
        room: RoomRequest,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    """
    Доступно под ролью - админ.
    Создание номера.
    :param hotel_id: id гостиницы
    :param room: номер - входящий JSON
    :param session: async сессия БД
    :return: новый номер. http response
    """
    room_exist = await RoomDAO.get_one(session, name=room.name)
    if room_exist:
        logger.error(RoomAlreadyExistsErr.detail, extra={"status_code": RoomAlreadyExistsErr.status_code})
        raise RoomAlreadyExistsErr

    return await RoomDAO.add(session, Room.add_id(hotel_id, room))


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
        room_id: int,
        hotel_id: int,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    """
    Получение номера по id.
    :param hotel_id: id гостиницы
    :param room_id: id номера
    :param session: async сессия БД
    :return: номера. http response
    """
    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        logger.error(HotelNotFoundErr.detail, extra={"status_code": HotelNotFoundErr.status_code})
        raise HotelNotFoundErr

    room = await RoomDAO.get_one(session, id=room_id)
    if not room:
        logger.error(RoomNotFoundErr.detail, extra={"status_code": RoomNotFoundErr.status_code})
        raise RoomNotFoundErr

    return room


@router.get("/{hotel_id}/rooms")
async def get_all_rooms_by_hotel(
        hotel_id: int,
        session: AsyncSession = Depends(get_session),
) -> List[RoomResponse]:
    """
    Получение всех номеров гостиницы.
    :param hotel_id: id гостиницы
    :param session: async сессия БД
    :return: список номеров. http response
    """
    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        logger.error(HotelNotFoundErr.detail, extra={"status_code": HotelNotFoundErr.status_code})
        raise HotelNotFoundErr

    rooms = await RoomDAO.get_all(session, hotel_id=hotel_id)
    if len(rooms) == 0:
        logger.error(NoRoomsErr.detail, extra={"status_code": NoRoomsErr.status_code})
        raise NoRoomsErr

    return rooms


@router.put("/{hotel_id}/rooms/{room_id}", dependencies=[Depends(admin_check)])
async def update_room_by_id(
        room_id: int,
        hotel_id: int,
        new_fields: RoomUpdateRequest,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    """
    Доступно под ролью - админ.
    Изменение номера по id.
    :param hotel_id: id гостиницы
    :param room_id: id номера
    :param new_fields: новые поля
    :param session: async сессия БД
    :return: измененный номер. http response
    """
    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        logger.error(HotelNotFoundErr.detail, extra={"status_code": HotelNotFoundErr.status_code})
        raise HotelNotFoundErr

    # проверка на полностью пустые поля
    if new_fields.is_empty():
        logger.error(EmptyFieldsToUpdateErr.detail, extra={"status_code": EmptyFieldsToUpdateErr.status_code})
        raise EmptyFieldsToUpdateErr

    room = await RoomDAO.get_one(session, id=room_id)
    if not room:
        logger.error(RoomNotFoundErr.detail, extra={"status_code": RoomNotFoundErr.status_code})
        raise RoomNotFoundErr

    # установка новых значений полей
    updated_fields: dict[str, Any] = set_new_fields(room, new_fields)
    return await RoomDAO.update(session, updated_fields, room_id)


@router.delete("/{hotel_id}/rooms/{room_id}", dependencies=[Depends(admin_check)])
async def delete_room_by_id(
        hotel_id: int,
        room_id: int,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    """
    Доступно под ролью - админ.
    Удаление комнаты по id.
    :param hotel_id: id гостиницы
    :param room_id: id комнаты
    :param session: async сессия БД
    :return: удаленная гостиница. http response
    """
    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        logger.error(HotelNotFoundErr.detail, extra={"status_code": HotelNotFoundErr.status_code})
        raise HotelNotFoundErr

    room = await RoomDAO.get_one(session, id=room_id)
    if not room:
        logger.error(RoomNotFoundErr.detail, extra={"status_code": RoomNotFoundErr.status_code})
        raise RoomNotFoundErr

    return await RoomDAO.delete(session, room_id)
