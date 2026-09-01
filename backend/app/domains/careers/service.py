"""Career Intelligence business logic."""

import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.assessments.models import AssessmentResult
from app.domains.careers.candidate_generation import CareerCandidateGenerator
from app.domains.careers.repository import CareerRepository
from app.domains.student.service import StudentService


class CareerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = CareerRepository(session)
        self.students = StudentService(session)

    async def list_careers(self, category_code: str | None = None):
        return await self.repo.list_active(category_code)

    async def get_career(self, career_id: uuid.UUID):
        career = await self.repo.get_detail(career_id)
        if not career:
            raise HTTPException(status_code=404, detail="Career not found.")
        return career

    async def generate_candidates(self, user_id: uuid.UUID, assessment_session_id: uuid.UUID | None = None):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")

        careers = await self.repo.list_active()

        result = None
        if assessment_session_id:
            result = await self._get_assessment_result(
                student.id, assessment_session_id
            )

        return CareerCandidateGenerator.generate(
            careers=careers,
            student=student,
            assessment_result=result,
        )

    async def _get_assessment_result(self, student_id: uuid.UUID, session_id: uuid.UUID):
        from app.domains.assessments.models import AssessmentSession

        result = await self.session.execute(
            select(AssessmentResult)
            .join(AssessmentSession, AssessmentSession.id == AssessmentResult.session_id)
            .where(
                AssessmentResult.session_id == session_id,
                AssessmentSession.student_id == student_id,
                AssessmentSession.status == "completed",
            )
        )
        return result.scalar_one_or_none()
