from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import UserNotFoundErr, EmptyFieldsToUpdateErr, NoUsersErr
from app.schemas.user import UserResponse, UserUpdateRequest
from app.storage.database import get_session
from app.storage.user import UserDAO
from app.utils import set_user_new_fields

# регистрация роута пользователя
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    Получение пользователя по id.
    :param user_id: id пользователя
    :param session: async сессия БД
    :return: пользователь. http response
    """
    user = await UserDAO.get_one(session, id=user_id)
    if not user:
        raise UserNotFoundErr

    return user


@router.get("")
async def get_all_users(
        session: AsyncSession = Depends(get_session),
) -> list[UserResponse]:
    """
    Получение всех пользователей.
    :param session: async сессия БД
    :return: список пользователей. http response
    """
    users = await UserDAO.get_all(session)
    if len(users) == 0:
        raise NoUsersErr

    return users


@router.put("/{user_id}")
async def update_user_by_id(
        user_id: int,
        new_fields: UserUpdateRequest,
        session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    Изменение пользователя по id.
    :param user_id: id пользователя
    :param new_fields: новые поля
    :param session: async сессия БД
    :return: измененный пользователь. http response
    """
    # проверка на полностью пустые поля
    if new_fields.is_empty():
        raise EmptyFieldsToUpdateErr

    user = await UserDAO.get_one(session, id=user_id)
    if not user:
        raise UserNotFoundErr

    # установка новых значений полей
    updated_fields: dict[str, Any] = set_user_new_fields(user, new_fields)
    return await UserDAO.update(session, updated_fields, user_id)


@router.delete("/{user_id}")
async def delete_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    Удаление пользователя по id.
    :param user_id: id пользователя
    :param session: async сессия БД
    :return: удаленный пользователь. http response
    """
    user = await UserDAO.get_one(session, id=user_id)
    if not user:
        raise UserNotFoundErr

    return await UserDAO.delete(session, user_id)
