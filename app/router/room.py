from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from app.errors import EmptyFieldsToUpdateErr, RoomAlreadyExistsErr, RoomNotFoundErr, NoRoomsErr
from app.schemas.room import RoomRequest, RoomResponse, RoomUpdateRequest
from app.storage.database import get_session
from app.storage.room import RoomDAO
from app.utils import set_new_fields

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.post("", status_code=201)
async def add_room(
        room: RoomRequest,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    room_exist = await RoomDAO.get_one(session, name=room.name)
    if room_exist:
        raise RoomAlreadyExistsErr

    return await RoomDAO.add(session, room.dict())


@router.get("/{room_id}")
async def get_room_by_id(
        room_id: int,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    room = await RoomDAO.get_one(session, id=room_id)
    if not room:
        raise RoomNotFoundErr

    return room


@router.get("")
async def get_all_rooms(
        session: AsyncSession = Depends(get_session),
) -> list[RoomResponse]:
    rooms = await RoomDAO.get_all(session)
    if len(rooms) == 0:
        raise NoRoomsErr

    return rooms


@router.put("/{room_id}")
async def update_room_by_id(
        room_id: int,
        new_fields: RoomUpdateRequest,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    # проверка на полностью пустые поля
    if new_fields.is_empty():
        raise EmptyFieldsToUpdateErr

    room = await RoomDAO.get_one(session, id=room_id)
    if not room:
        raise RoomNotFoundErr

    # установка новых значений полей
    updated_fields: dict[str, Any] = set_new_fields(room, new_fields)
    return await RoomDAO.update(session, updated_fields, room_id)


@router.delete("/{room_id}")
async def delete_room_by_id(
        room_id: int,
        session: AsyncSession = Depends(get_session),
) -> RoomResponse:
    room = await RoomDAO.get_one(session, id=room_id)
    if not room:
        raise RoomNotFoundErr

    return await RoomDAO.delete(session, room_id)
