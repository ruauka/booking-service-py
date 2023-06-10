from datetime import date, datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, Query
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import auth_user
from app.errors import (
    BookingNotFoundErr,
    EmptyFieldsToUpdateErr,
    NoAvailableRoomsErr,
    NoBookingsErr,
)
from app.logger import logger
from app.models.user import User
from app.schemas.booking import BookingResponse, BookingUpdateRequest
from app.storage.booking import BookingDAO
from app.storage.database import get_session
from app.tasks.tasks import send_booking_confirmation_email
from app.utils import set_new_fields

# регистрация роута бронирования
router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("", status_code=201)
async def add_booking(
        room_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
):
    """
    Создание нового бронирования комнаты по ее id.
    :param room_id: id комнаты
    :param date_from: дата бронирования 'с'
    :param date_to: дата бронирования 'по'
    :param user: пользователь из БД, полученный после авторизации
    :param session: async сессия БД
    :return: новое бронирование
    """
    # получение свободных комнат по id комнаты в указанные даты и ифно по гостинице
    room_hotel_info = await BookingDAO.get_free_rooms(session, room_id, date_from, date_to)
    # проверка на свободные комнаты
    if room_hotel_info[0]["free_rooms"] <= 0:
        logger.error(NoAvailableRoomsErr.detail, extra={"status_code": NoAvailableRoomsErr.status_code})
        raise NoAvailableRoomsErr
    booking = await BookingDAO.add(session, user.id, room_id, date_from, date_to)
    # парсинг ответа алхимии в словарь для celery
    booking_dict = parse_obj_as(BookingResponse, booking).dict()
    # фоновый вызов celery
    send_booking_confirmation_email.delay(
        booking_dict,
        user.email,
        room_hotel_info[0]["room_name"],
        room_hotel_info[0]["hotel_name"]
    )
    # выходная валидация не требуется, booking_dict провалидирован parse_obj_as()
    return booking_dict


@router.get("/{booking_id}")
async def get_booking_by_id(
        booking_id: int,
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
) -> BookingResponse:
    """
    Требуется авторизация.
    Получение бронирования по id.
    :param booking_id: id бронирования
    :param user: пользователь из БД, полученный после авторизации
    :param session: async сессия БД
    :return: бронирование. http response
    """
    booking = await BookingDAO.get_one(session, id=booking_id, user_id=user.id)
    if not booking:
        logger.error(BookingNotFoundErr.detail, extra={"status_code": BookingNotFoundErr.status_code})
        raise BookingNotFoundErr

    return booking


@router.get("")
async def get_all_bookings_by_user(
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
) -> List[BookingResponse]:
    """
    Требуется авторизация.
    Получение всех бронирований пользователя.
    :param user: пользователь из БД, полученный после авторизации
    :param session: async сессия БД
    :return: список бронирований. http response
    """
    bookings = await BookingDAO.get_all(session, user_id=user.id)
    if len(bookings) == 0:
        logger.error(NoBookingsErr.detail, extra={"status_code": NoBookingsErr.status_code})
        raise NoBookingsErr

    return bookings


@router.put("/{booking_id}")
async def update_booking_by_id(
        booking_id: int,
        new_fields: BookingUpdateRequest,
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
) -> BookingResponse:
    """
    Требуется авторизация.
    Изменение бронирования пользователя по id.
    :param booking_id: id бронирования
    :param new_fields: новые поля
    :param user: пользователь из БД, полученный после авторизации
    :param session: async сессия БД
    :return: измененное бронирование. http response
    """
    # проверка на полностью пустые поля
    if new_fields.is_empty():
        logger.error(EmptyFieldsToUpdateErr.detail, extra={"status_code": EmptyFieldsToUpdateErr.status_code})
        raise EmptyFieldsToUpdateErr

    booking = await BookingDAO.get_one(session, id=booking_id, user_id=user.id)
    if not booking:
        logger.error(BookingNotFoundErr.detail, extra={"status_code": BookingNotFoundErr.status_code})
        raise BookingNotFoundErr

    # установка новых значений полей
    updated_fields: dict[str, Any] = set_new_fields(booking, new_fields)
    # получение свободных комнат по id комнаты в указанные даты
    free_rooms = await BookingDAO.get_free_rooms(
        session,
        room_id=updated_fields.get("room_id"),
        date_from=updated_fields.get("date_from"),
        date_to=updated_fields.get("date_to")
    )
    # проверка на свободные комнаты
    if free_rooms <= 0:
        logger.error(NoAvailableRoomsErr.detail, extra={"status_code": NoAvailableRoomsErr.status_code})
        raise NoAvailableRoomsErr

    return await BookingDAO.update(session, updated_fields, booking_id)


@router.delete("/{booking_id}")
async def delete_booking_by_id(
        booking_id: int,
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
) -> BookingResponse:
    """
    Требуется авторизация.
    Удаление бронирования пользователя по id.
    :param booking_id: id бронирования
    :param user: пользователь из БД, полученный после авторизации
    :param session: async сессия БД
    :return: удаленное бронирование
    """
    booking = await BookingDAO.get_one(session, user_id=user.id, id=booking_id)
    if not booking:
        logger.error(BookingNotFoundErr.detail, extra={"status_code": BookingNotFoundErr.status_code})
        raise BookingNotFoundErr

    return await BookingDAO.delete(session, booking_id)
