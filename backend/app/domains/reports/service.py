"""Reports business workflows."""

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.reports.repository import ReportRepository
from app.domains.student.service import StudentService


class ReportService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ReportRepository(session)
        self.students = StudentService(session)

    async def _student(self, user_id):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")
        return student

    async def list_reports(self, user_id):
        student = await self._student(user_id)
        return await self.repo.list_for_student(student.id)

    async def get_report(self, user_id, report_id):
        student = await self._student(user_id)
        report = await self.repo.get(student.id, report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found.")
        return report

    async def create_report(self, user_id, data):
        student = await self._student(user_id)
        report = await self.repo.create(student.id, data)
        await self.session.commit()
        return await self.repo.get(student.id, report.id)
