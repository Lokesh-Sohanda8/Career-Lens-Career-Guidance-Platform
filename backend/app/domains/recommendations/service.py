"""Recommendation business workflows."""

import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.assessments.models import AssessmentResult, AssessmentSession
from app.domains.careers.models import Career
from app.domains.recommendations.engine import RecommendationEngineV1
from app.domains.recommendations.repository import RecommendationRepository
from app.domains.skills.models import StudentSkillEvidence
from app.domains.student.service import StudentService


class RecommendationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = RecommendationRepository(session)
        self.students = StudentService(session)

    async def generate(self, user_id, assessment_session_id=None, limit=5):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")

        assessment_result = None
        if assessment_session_id:
            assessment_result = await self._assessment_result(student.id, assessment_session_id)

        careers = await self._careers()
        skill_evidence = await self._skill_evidence(student.id)

        ranked = RecommendationEngineV1.recommend(
            careers=careers,
            student=student,
            skill_evidence=skill_evidence,
            assessment_result=assessment_result,
            limit=limit,
        )

        run = await self.repo.create_run(
            student.id, assessment_session_id, RecommendationEngineV1.VERSION
        )
        for code, weight in RecommendationEngineV1.FACTORS.items():
            await self.repo.add_factor(
                run.id,
                code,
                weight,
                {
                    "assessment_fit": "Alignment with available assessment traits.",
                    "interest_fit": "Alignment with explicitly recorded student interests.",
                    "skill_fit": "Coverage of explicit career skill requirements.",
                }[code],
            )
        for item in ranked:
            await self.repo.add_item(run.id, item)

        await self.session.commit()
        return run, ranked

    async def get(self, user_id, run_id):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")
        run = await self.repo.get_run(run_id, student.id)
        if not run:
            raise HTTPException(status_code=404, detail="Recommendation run not found.")
        return run

    async def history(self, user_id):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")
        return await self.repo.history(student.id)

    async def _careers(self):
        result = await self.session.execute(
            select(Career)
            .where(Career.is_active.is_(True))
            .options(selectinload(Career.category), selectinload(Career.requirements))
        )
        return list(result.scalars().all())

    async def _skill_evidence(self, student_id):
        result = await self.session.execute(
            select(StudentSkillEvidence).where(StudentSkillEvidence.student_id == student_id)
        )
        return list(result.scalars().all())

    async def _assessment_result(self, student_id, session_id):
        result = await self.session.execute(
            select(AssessmentResult)
            .join(AssessmentSession, AssessmentSession.id == AssessmentResult.session_id)
            .where(
                AssessmentResult.session_id == session_id,
                AssessmentSession.student_id == student_id,
                AssessmentSession.status == "completed",
            )
        )
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Completed assessment result not found.")
        return item
