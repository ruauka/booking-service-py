from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from app.auth.auth import get_password_hash, verify_user, create_JWT_token
from app.auth.dependencies import auth_user
from app.errors import UserAlreadyExistsErr, IncorrectEmailOrPasswordErr
from app.storage.database import get_session
from app.schemas.user import UserRequest, UserResponse
from app.models.user import User
from app.storage.user import UserDAO

# регистрация роута авторизации
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/registration", status_code=201)
async def register_user(
        user: UserRequest,
        session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    Регистрация пользователя.
    :param user: пользователь - входящий JSON
    :param session: async сессия БД
    :return: новый пользователь. http response
    """
    exist_user: User = await UserDAO.get_one(session, email=user.email)
    if exist_user:
        raise UserAlreadyExistsErr

    hashed_password: str = get_password_hash(user.password)
    return await UserDAO.add(session, user.hash_pass_replace(hashed_password))


@router.post("/login")
async def login(
        user: UserRequest,
        response: Response,
        session: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    """
    Аутентификация пользователя.
    :param user: пользователь - входящий JSON
    :param response: http ответ, в который кладется JWT-токен
    :param session: async сессия БД
    :return: JWT-токен в виде JSON и добавленная в хедеры кука "access_token", в которой лежит JWT-токен
    """
    user = await verify_user(session, user.email, user.password)
    if not user:
        raise IncorrectEmailOrPasswordErr

    token = create_JWT_token({"sub": str(user.id)})
    # response добавляет в ответ куку, возращать что то в ответе не требуется
    response.set_cookie("JWT", token, httponly=True)
    return {"JWT": token}


@router.post("/logout")
async def logout_user(response: Response) -> dict[str, str]:
    """
    Логаут пользователя. Удаление из хедера куки с JWT-токеном
    :param response: http ответ, из куки которого удаляется JWT-токен
    :return: информационное сообщение
    """
    response.delete_cookie("JWT")
    return {"message": "logged out"}


@router.get("/me")
async def current_login_user(user: User = Depends(auth_user)) -> UserResponse:
    """
    Требуется авторизация.
    Проверка, кто залогинен.
    :param user: пользователь из БД, полученный после авторизации
    :return: пользователь JSON
    """
    # return user
    # parse_obj_as - валидация, вместо -> UserResponse
    return parse_obj_as(UserResponse, user)
