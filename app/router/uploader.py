import sqlparse
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.storage.database import get_session
from app.storage.uploader import upload_sql_queries

router = APIRouter(
    prefix="/upload",
    tags=["DB Upload"],
)


@router.post("/sql")
async def upload_from_sql_file(file: UploadFile, session: AsyncSession = Depends(get_session)):
    byte_queries = await file.read()
    queries = sqlparse.split(
        sqlparse.format(
            byte_queries.decode("utf-8"),
            strip_comments=True)
    )
    await upload_sql_queries(session, queries)
    return "sql scripts loaded successfully"
