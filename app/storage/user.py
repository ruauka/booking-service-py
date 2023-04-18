from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.models import User
from app.schemas.user import UserRequest


# async def add(self, user_in: UserRequest, session: AsyncSession):
#     user = User(email=user_in.email, hashed_password=user_in.password)
#     query = insert(User).values(**user.to_dict())
#     await session.execute(query)
#     await session.commit()

# async def get(self, user_id: int, session: AsyncSession):
#     user_id = {
#         "id": user_id
#     }
#
#     query = select(User).filter_by(**user_id)
#     result = await session.execute(query)
#     return result.scalar_one_or_none()
