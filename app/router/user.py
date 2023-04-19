from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserResponse
from app.storage.database import get_session
from app.storage.user import UserDAO

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
    return UserResponse(id=user.id, email=user.email)


@router.get("")
async def get_all_users(
        session: AsyncSession = Depends(get_session),
) -> list[UserResponse]:
    users = await UserDAO.get_all(session)
    return UserResponse.all_resp(users)
