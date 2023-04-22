from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from app.errors import HotelAlreadyExistsErr, HotelNotFoundErr, NoHotelsErr
from app.schemas.hotel import HotelRequest, HotelResponse
from app.storage.database import get_session
from app.storage.hotel import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.post("")
async def add_hotel(
        hotel: HotelRequest,
        session: AsyncSession = Depends(get_session),
):
    hotel_exist = await HotelDAO.get_one(session, name=hotel.name)
    if hotel_exist:
        raise HotelAlreadyExistsErr

    new_hotel = await HotelDAO.add(session, hotel.dict())
    return parse_obj_as(HotelResponse, new_hotel)


@router.get("/{hotel_id}")
async def get_hotel_by_id(
        hotel_id: int,
        session: AsyncSession = Depends(get_session),
) -> HotelResponse:
    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        raise HotelNotFoundErr

    return parse_obj_as(HotelResponse, hotel)


@router.get("")
async def get_all_hotels(
        session: AsyncSession = Depends(get_session),
) -> list[HotelResponse]:
    hotels = await HotelDAO.get_all(session)
    if len(hotels) == 0:
        raise NoHotelsErr

    return parse_obj_as(List[HotelResponse], hotels)
