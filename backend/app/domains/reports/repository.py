"""Reports persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.reports.models import Report, ReportSection


class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_for_student(self, student_id):
        result = await self.session.execute(
            select(Report)
            .where(Report.student_id == student_id)
            .order_by(Report.generated_at.desc())
        )
        return list(result.scalars().all())

    async def get(self, student_id, report_id):
        result = await self.session.execute(
            select(Report)
            .where(Report.id == report_id, Report.student_id == student_id)
            .options(selectinload(Report.sections))
        )
        return result.scalar_one_or_none()

    async def create(self, student_id, data):
        report = Report(
            student_id=student_id,
            report_type=data.report_type,
            title=data.title,
            source_snapshot=data.source_snapshot,
            version=1,
            status="generated",
        )
        self.session.add(report)
        await self.session.flush()

        for section in data.sections:
            self.session.add(
                ReportSection(report_id=report.id, **section.model_dump())
            )
        await self.session.flush()
        return report
