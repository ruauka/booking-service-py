from datetime import date
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import UnknownErr
from app.logger import logger
from app.models.booking import Booking
from app.models.room import Room
from app.storage.dao import BaseDAO


class RoomDAO(BaseDAO):
    """
    Класс для использования DAO методов.
    """
    model = Room

    @classmethod
    async def get_rooms_by_time(cls, session: AsyncSession, hotel_id: int, date_from: date, date_to: date) -> Any:
        """
        Получение списока всех свободных для бронирования номеров определенной гостиницы.
        :param session: session: async сессия БД
        :param hotel_id: id гостиницы
        :param date_from: дата бронирования 'с'
        :param date_to: дата бронирования 'по'
        :return: список номеров
        """
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                  (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            GROUP BY room_id
        )
        SELECT
            -- все столбцы из rooms,
            (quantity - COALESCE(rooms_booked, 0)) AS rooms_left FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE hotel_id = 1
        """
        try:
            booked_rooms = (
                select(Booking.room_id, func.count(Booking.room_id).label("rooms_booked"))
                .select_from(Booking)
                .where(
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_from <= date_to,
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to > date_from,
                        ),
                    ),
                )
                .group_by(Booking.room_id)
                .cte("booked_rooms")
            )

            get_rooms = (
                select(
                    Room.__table__.columns,
                    (Room.price * (date_to - date_from).days).label("total_cost"),
                    (Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left"),
                )
                .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
                .where(
                    Room.hotel_id == hotel_id
                )
            )

            # logger.debug(get_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms = await session.execute(get_rooms)
            return rooms.mappings().all()
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(err, Exception):
                msg = "Unknown Exc: Cannot add booking"
            extra = {
                "hotel_id": hotel_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra)
