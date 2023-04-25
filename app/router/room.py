from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from app.errors import HotelAlreadyExistsErr, HotelNotFoundErr, NoHotelsErr, EmptyFieldsToUpdateErr, \
    RoomAlreadyExistsErr, RoomNotFoundErr, NoRoomsErr
from app.schemas.hotel import HotelRequest, HotelResponse, HotelUpdateRequest
from app.schemas.room import RoomRequest, RoomResponse
from app.storage.database import get_session
from app.storage.hotel import HotelDAO
from app.storage.room import RoomDAO
from app.utils import set_new_fields

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.post("")
async def add_room(
        room: RoomRequest,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    room_exist = await RoomDAO.get_one(session, name=room.name)
    if room_exist:
        raise RoomAlreadyExistsErr

    new_room = await RoomDAO.add(session, room.dict())
    return parse_obj_as(RoomResponse, new_room)


@router.get("/{room_id}")
async def get_room_by_id(
        room_id: int,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    room = await RoomDAO.get_one(session, id=room_id)
    if not room:
        raise RoomNotFoundErr

    return parse_obj_as(RoomResponse, room)


@router.get("")
async def get_all_rooms(
        session: AsyncSession = Depends(get_session),
) -> list[RoomResponse]:
    rooms = await RoomDAO.get_all(session)
    if len(rooms) == 0:
        raise NoRoomsErr

    return parse_obj_as(List[RoomResponse], rooms)
