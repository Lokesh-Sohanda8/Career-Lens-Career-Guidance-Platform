"""Reports endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.reports.schemas import ReportCreate, ReportRead, ReportSummaryRead
from app.domains.reports.service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("", response_model=list[ReportSummaryRead])
async def list_reports(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ReportService(db).list_reports(user.id)


@router.get("/{report_id}", response_model=ReportRead)
async def get_report(
    report_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ReportService(db).get_report(user.id, report_id)


@router.post("", response_model=ReportRead, status_code=201)
async def create_report(
    payload: ReportCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ReportService(db).create_report(user.id, payload)
