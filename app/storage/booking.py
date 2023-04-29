from datetime import date
from fastapi import HTTPException, status
from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import UnknownErr
from app.models.booking import Booking
from app.models.room import Room
from app.storage.dao import BaseDAO
from app.storage.database import engine


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add(cls, session: AsyncSession, user_id: int, room_id: int, date_from: date, date_to: date):
        """"""
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

            if free_rooms > 0:
                get_room_price_query = select(Room.price).filter_by(id=room_id)
                room_price = await session.execute(get_room_price_query)
                room_price: int = room_price.scalar()
                add_booking_query = (
                    insert(Booking)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=room_price,
                    )
                    .returning(Booking)
                )

                new_booking = await session.execute(add_booking_query)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(err),
                )
            elif isinstance(err, Exception):
                raise UnknownErr
