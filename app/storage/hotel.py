from datetime import date
from typing import Any
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.errors import UnknownErr
from app.models.booking import Booking
from app.models.hotel import Hotel
from app.models.room import Room
from app.storage.dao import BaseDAO


class HotelDAO(BaseDAO):
    """
    Класс для использования DAO методов.
    """
    model = Hotel

    @classmethod
    async def get_hotels_by_location(cls, session: AsyncSession, location: str, date_from: date, date_to: date) -> Any:
        """
        Получение списока отелей по заданным параметрам, причем в отеле должен быть минимум 1 свободный номер.
        :param session: session: async сессия БД
        :param location: местонахождение гостиницы
        :param date_from: дата бронирования 'с'
        :param date_to: дата бронирования 'по'
        :return:
        """
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE 
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            GROUP BY room_id
        ),
        booked_hotels AS (
            SELECT hotel_id, SUM(rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left
            FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            GROUP BY hotel_id
        )
        SELECT * FROM hotels
        LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
        WHERE rooms_left > 0 AND location LIKE '%Алтай%';
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

            booked_hotels = (
                select(Room.hotel_id, func.sum(
                    Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
                ).label("rooms_left"))
                .select_from(Room)
                .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
                .group_by(Room.hotel_id)
                .cte("booked_hotels")
            )

            get_hotels_with_rooms = (
                # Hotels.__table__.columns - алхимия отдает все столбцы по одному, как отдельный атрибут.
                # Если передать всю модель Hotels и один дополнительный столбец rooms_left,
                # то будет проблематично для Pydantic распарсить такую структуру данных.
                # Используется hotels_with_rooms.mappings().all() не hotels_with_rooms.scalars().all()
                select(
                    Hotel.__table__.columns,
                    booked_hotels.c.rooms_left,
                )
                .join(booked_hotels, booked_hotels.c.hotel_id == Hotel.id, isouter=True)
                .where(
                    and_(
                        booked_hotels.c.rooms_left > 0,
                        Hotel.location.like(f"%{location}%"),
                    )
                )
            )

            # logger.debug(get_hotels_with_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(err),
                )
            elif isinstance(err, Exception):
                raise UnknownErr
