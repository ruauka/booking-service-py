from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from app.errors import HotelAlreadyExistsErr, HotelNotFoundErr, NoHotelsErr, EmptyFieldsToUpdateErr
from app.schemas.hotel import HotelRequest, HotelResponse, HotelUpdateRequest
from app.storage.database import get_session
from app.storage.hotel import HotelDAO
from app.utils import set_new_fields

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


@router.put("/{hotel_id}")
async def update_hotel_by_id(
        hotel_id: int,
        new_fields: HotelUpdateRequest,
        session: AsyncSession = Depends(get_session),
):
    # проверка на полностью пустые поля
    if new_fields.is_empty():
        raise EmptyFieldsToUpdateErr

    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        raise HotelNotFoundErr

    # установка новых значений полей
    updated_fields: dict[str, Any] = set_new_fields(hotel, new_fields)
    new_hotel = await HotelDAO.update(session, updated_fields, hotel_id)
    return parse_obj_as(HotelResponse, new_hotel)


@router.delete("/{hotel_id}")
async def delete_user_by_id(
        hotel_id: int,
        session: AsyncSession = Depends(get_session),
) -> HotelResponse:
    hotel = await HotelDAO.get_one(session, id=hotel_id)
    if not hotel:
        raise HotelNotFoundErr

    hotels = await HotelDAO.delete(session, hotel_id)
    return parse_obj_as(HotelResponse, hotels)
