from datetime import date
from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import UnknownErr
from app.models.booking import Booking
from app.models.room import Room
from app.storage.dao import BaseDAO


class BookingDAO(BaseDAO):
    """
    Класс для использования DAO методов.
    """
    model = Booking

    @classmethod
    async def add(cls, session: AsyncSession, user_id: int, room_id: int, date_from: date, date_to: date) -> Any:
        """
        Добавление бронирования по условиям.
        :param session: async сессия БД
        :param user_id: id пользователя
        :param room_id: id комнаты
        :param date_from: дата бронирования 'с'
        :param date_to: дата бронирования 'по'
        :return: новое бронирование
        """
        try:
            add_booking_query = (
                insert(Booking)
                .values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=await cls.get_room_price(session, room_id),
                )
                .returning(Booking)
            )

            new_booking = await session.execute(add_booking_query)
            await session.commit()
            return new_booking.scalar()
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(err),
                )
            elif isinstance(err, Exception):
                raise UnknownErr

    @classmethod
    async def get_room_price(cls, session: AsyncSession, room_id: int) -> int:
        """
        Получение цены аренды комнаты за сутки.
        :param session: async сессия БД
        :param room_id: id комнаты
        :return: цена комнаты
        """
        get_room_price_query = select(Room.price).filter_by(id=room_id)
        room_price = await session.execute(get_room_price_query)
        return room_price.scalar()

    @classmethod
    async def get_free_rooms(cls, session: AsyncSession, room_id: int, date_from: date, date_to: date) -> int:
        """
        Получение свободных комнат по id комнаты в указанные даты
        :param session: async сессия БД
        :param room_id: id комнаты
        :param date_from: дата бронирования 'с'
        :param date_to: дата бронирования 'по'
        :return: количество свободных комнат
        """
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1
            AND(
                (date_from BETWEEN '2023-05-15' AND '2023-06-20')
                OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            )
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id)
        FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        try:
            # забронированные комнаты (таблица)
            booked_rooms = (
                select(Booking)
                .where(
                    and_(
                        Booking.room_id == room_id,
                        or_(
                            and_(
                                Booking.date_from.between(date_from, date_to)
                            ),
                            and_(
                                Booking.date_from <= date_from,
                                Booking.date_to > date_from,
                            ),
                        ),
                    )
                ).cte("booked_rooms")
            )

            """
            SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id
            """

            # количество свободных комнат
            free_rooms_quant_query = (
                select(Room.quantity - func.count(booked_rooms.c.room_id))
                .select_from(Room)
                .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
                .where(Room.id == room_id)
                .group_by(Room.quantity, booked_rooms.c.room_id)
            )

            # распечатка sql запроса
            # print(remaining_rooms_query.compile(engine, compile_kwargs={"literal_binds": True}))

            free_rooms = await session.execute(free_rooms_quant_query)
            free_rooms: int = free_rooms.scalar()
            return free_rooms
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(err),
                )
            elif isinstance(err, Exception):
                raise UnknownErr
