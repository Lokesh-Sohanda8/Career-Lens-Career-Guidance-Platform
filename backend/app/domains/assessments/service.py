"""Assessment business workflows."""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.assessments.repository import AssessmentRepository
from app.domains.assessments.scoring import AssessmentScoringEngine


class AssessmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AssessmentRepository(session)

    async def list_active(self):
        return await self.repo.list_active()

    async def get_detail(self, assessment_id: uuid.UUID):
        version = await self.repo.get_published_detail(assessment_id)
        if not version:
            raise HTTPException(status_code=404, detail="Published assessment not found.")
        return version

    async def start(self, student_id: uuid.UUID, assessment_id: uuid.UUID):
        version = await self.repo.get_published_detail(assessment_id)
        if not version:
            raise HTTPException(status_code=404, detail="Published assessment not found.")
        item = await self.repo.create_session(student_id, version.id)
        await self.session.commit()
        return item

    async def save_response(self, student_id: uuid.UUID, session_id: uuid.UUID, question_id: uuid.UUID, option_id: uuid.UUID):
        session = await self.repo.get_session(session_id)
        if not session or session.student_id != student_id:
            raise HTTPException(status_code=404, detail="Assessment session not found.")
        if session.status != "in_progress":
            raise HTTPException(status_code=409, detail="Assessment session is no longer active.")

        version = await self.repo.get_version(session.assessment_version_id)
        question = next((q for q in version.questions if q.id == question_id), None)
        if not question:
            raise HTTPException(status_code=400, detail="Question does not belong to this assessment.")
        option = next((o for o in question.options if o.id == option_id), None)
        if not option:
            raise HTTPException(status_code=400, detail="Option does not belong to this question.")

        response = await self.repo.save_response(session_id, question_id, option_id)
        await self.session.commit()
        return response

    async def complete(self, student_id: uuid.UUID, session_id: uuid.UUID):
        session = await self.repo.get_session(session_id)
        if not session or session.student_id != student_id:
            raise HTTPException(status_code=404, detail="Assessment session not found.")
        if session.status != "in_progress":
            raise HTTPException(status_code=409, detail="Assessment session is no longer active.")

        version = await self.repo.get_version(session.assessment_version_id)
        required = {q.id for q in version.questions if q.is_required}
        answered = {r.question_id for r in session.responses}
        missing = required - answered
        if missing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Assessment is incomplete. Missing {len(missing)} required response(s).",
            )

        payload = AssessmentScoringEngine.score(version, session.responses)
        now = datetime.now(timezone.utc)
        session.status = "completed"
        session.completed_at = now
        result = await self.repo.create_result(
            session_id=session.id,
            scoring_version=version.scoring_version,
            payload=payload,
            completed_at=now,
        )
        await self.session.commit()
        return session, result
