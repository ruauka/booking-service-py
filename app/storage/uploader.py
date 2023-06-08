from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import UnknownErr


async def upload_sql_queries(session: AsyncSession, queries: list[str]) -> None:
    """
    Загрузка в БД sql-запросов.
    :param session: async сессия БД
    :param queries: список из sql-запросов
    :return: None
    """
    try:
        for query in queries:
            await session.execute(text(query))
        await session.commit()
    except (SQLAlchemyError, Exception) as err:
        if isinstance(err, SQLAlchemyError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(err),
            )
        elif isinstance(err, Exception):
            raise UnknownErr
