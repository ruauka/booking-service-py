from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as

from app.auth.auth import get_password_hash, verify_user, create_access_token
from app.auth.dependencies import auth_user
from app.errors import UserAlreadyExistsErr, IncorrectEmailOrPasswordErr
from app.storage.database import get_session
from app.schemas.user import UserRequest, UserResponse
from app.models.user import User
from app.storage.user import UserDAO

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/registration", status_code=201)
async def register_user(
        user: UserRequest,
        session: AsyncSession = Depends(get_session),
) -> UserResponse:
    exist_user = await UserDAO.get_one(session, email=user.email)
    if exist_user:
        raise UserAlreadyExistsErr

    hashed_password = get_password_hash(user.password)
    return await UserDAO.add(session, user.encode(hashed_password))


@router.post("/login")
async def login(
        user: UserRequest,
        response: Response,
        session: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    user = await verify_user(session, user.email, user.password)
    if not user:
        raise IncorrectEmailOrPasswordErr

    token = create_access_token({"sub": str(user.id)})
    # response добавляет в ответ куку, возращать что то в ответе не требуется
    response.set_cookie("access_token", token, httponly=True)
    return {"JWT": token}


@router.post("/logout")
async def logout_user(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"message": "logged out"}


@router.get("/me")
async def read_users_me(user: User = Depends(auth_user)) -> UserResponse:
    # return user
    return parse_obj_as(UserResponse, user)