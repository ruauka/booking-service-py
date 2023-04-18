from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.database import get_session
from app.schemas.user import UserRequest
from app.models.user import User
from app.storage.user import UserDAO

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/registration")
async def register_user(
        user: UserRequest,
        session: AsyncSession = Depends(get_session),
):
    resp = await UserDAO.add(session, User.parse(user))
    return resp


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_session),
):
    resp = await UserDAO.get_one(session, id=user_id)
    return resp


@router.get("")
async def get_all_users(
        session: AsyncSession = Depends(get_session),
):
    resp = await UserDAO.get_all(session)
    return resp
