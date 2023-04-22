from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from app.errors import UserNotFoundErr, EmptyFieldsToUpdateErr, NoUsersErr
from app.schemas.user import UserResponse, UserUpdateRequest
from app.storage.database import get_session
from app.storage.user import UserDAO
from app.utils import set_user_new_fields

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_session),
) -> UserResponse:
    user = await UserDAO.get_one(session, id=user_id)
    if not user:
        raise UserNotFoundErr

    return parse_obj_as(UserResponse, user)


@router.get("")
async def get_all_users(
        session: AsyncSession = Depends(get_session),
) -> list[UserResponse]:
    users = await UserDAO.get_all(session)
    if len(users) == 0:
        raise NoUsersErr

    return parse_obj_as(List[UserResponse], users)


@router.put("/{user_id}")
async def update_user_by_id(
        user_id: int,
        new_fields: UserUpdateRequest,
        session: AsyncSession = Depends(get_session),
) -> UserResponse:
    # проверка на полностью пустые поля
    if not new_fields.empty_check():
        raise EmptyFieldsToUpdateErr

    user = await UserDAO.get_one(session, id=user_id)
    if not user:
        raise UserNotFoundErr

    # установка новых значений полей
    updated_fields: dict[str, Any] = set_user_new_fields(user, new_fields)
    new_user = await UserDAO.update(session, updated_fields, user_id)
    return parse_obj_as(UserResponse, new_user)


@router.delete("/{user_id}")
async def delete_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_session),
) -> UserResponse:
    user = await UserDAO.get_one(session, id=user_id)
    if not user:
        raise UserNotFoundErr

    users = await UserDAO.delete(session, user_id)
    return parse_obj_as(UserResponse, users)
