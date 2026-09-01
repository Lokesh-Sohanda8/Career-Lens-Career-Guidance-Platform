from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.session import check_database_connection, get_db_session

router = APIRouter(tags=["system"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness(_: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    if not await check_database_connection():
        return {"status": "not_ready"}
    return {"status": "ready"}
