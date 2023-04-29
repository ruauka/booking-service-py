from datetime import date
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from app.auth.dependencies import auth_user
from app.errors import NoBookingsErr, NoAvailableRoomsErr, BookingNotFoundErr
from app.models.user import User
from app.schemas.booking import BookingResponse
from app.storage.booking import BookingDAO
from app.storage.database import get_session

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("", status_code=201)
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
) -> BookingResponse:
    booking = await BookingDAO.add(session, user.id, room_id, date_from, date_to)
    if not booking:
        raise NoAvailableRoomsErr

    return parse_obj_as(BookingResponse, booking)


@router.get("/{booking_id}")
async def get_booking_by_id(
        booking_id: int,
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
) -> BookingResponse:
    booking = await BookingDAO.get_one(session, id=booking_id, user_id=user.id)
    if not booking:
        raise BookingNotFoundErr

    return parse_obj_as(BookingResponse, booking)


@router.get("")
async def get_all_bookings_by_user(
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
) -> list[BookingResponse]:
    bookings = await BookingDAO.get_all(session, user_id=user.id)
    if len(bookings) == 0:
        raise NoBookingsErr

    return parse_obj_as(List[BookingResponse], bookings)


@router.delete("/{booking_id}")
async def delete_booking_by_id(
        booking_id: int,
        user: User = Depends(auth_user),
        session: AsyncSession = Depends(get_session),
) -> BookingResponse:
    booking = await BookingDAO.get_one(session, user_id=user.id, id=booking_id)
    if not booking:
        raise BookingNotFoundErr

    booking = await BookingDAO.delete(session, booking_id)
    return parse_obj_as(BookingResponse, booking)
