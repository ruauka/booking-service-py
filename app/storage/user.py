from app.models.user import User
from app.storage.dao import BaseDAO


class UserDAO(BaseDAO):
    model = User

    # @classmethod
    # async def get_all(cls, session: AsyncSession, **filters) -> Any:
    #     query = select(cls.model).filter_by(**filters)
    #     result = await session.execute(query)
    #     return result.scalars().all()
