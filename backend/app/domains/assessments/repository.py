"""Assessment persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.assessments.models import (
    Assessment, AssessmentDimension, AssessmentOption, AssessmentQuestion,
    AssessmentResponse, AssessmentResult, AssessmentSession, AssessmentVersion,
)


class AssessmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_active(self):
        result = await self.session.execute(
            select(Assessment).where(Assessment.is_active.is_(True)).order_by(Assessment.name)
        )
        return list(result.scalars().all())

    async def get_published_detail(self, assessment_id: uuid.UUID):
        result = await self.session.execute(
            select(AssessmentVersion)
            .where(
                AssessmentVersion.assessment_id == assessment_id,
                AssessmentVersion.is_published.is_(True),
            )
            .options(
                selectinload(AssessmentVersion.assessment),
                selectinload(AssessmentVersion.dimensions),
                selectinload(AssessmentVersion.questions).selectinload(AssessmentQuestion.options),
            )
            .order_by(AssessmentVersion.version.desc())
        )
        return result.scalars().first()

    async def get_version(self, version_id: uuid.UUID):
        result = await self.session.execute(
            select(AssessmentVersion)
            .where(AssessmentVersion.id == version_id)
            .options(
                selectinload(AssessmentVersion.questions).selectinload(AssessmentQuestion.options),
                selectinload(AssessmentVersion.dimensions),
            )
        )
        return result.scalar_one_or_none()

    async def get_session(self, session_id: uuid.UUID):
        result = await self.session.execute(
            select(AssessmentSession)
            .where(AssessmentSession.id == session_id)
            .options(
                selectinload(AssessmentSession.responses),
                selectinload(AssessmentSession.result),
            )
        )
        return result.scalar_one_or_none()

    async def create_session(self, student_id: uuid.UUID, version_id: uuid.UUID):
        item = AssessmentSession(student_id=student_id, assessment_version_id=version_id)
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def get_response(self, session_id: uuid.UUID, question_id: uuid.UUID):
        result = await self.session.execute(
            select(AssessmentResponse).where(
                AssessmentResponse.session_id == session_id,
                AssessmentResponse.question_id == question_id,
            )
        )
        return result.scalar_one_or_none()

    async def save_response(self, session_id: uuid.UUID, question_id: uuid.UUID, option_id: uuid.UUID):
        response = await self.get_response(session_id, question_id)
        if response:
            response.selected_option_id = option_id
        else:
            response = AssessmentResponse(
                session_id=session_id,
                question_id=question_id,
                selected_option_id=option_id,
            )
            self.session.add(response)
        await self.session.flush()
        return response

    async def create_result(self, session_id: uuid.UUID, scoring_version: str, payload: dict, completed_at):
        result = AssessmentResult(
            session_id=session_id,
            scoring_version=scoring_version,
            result_payload=payload,
            completed_at=completed_at,
        )
        self.session.add(result)
        await self.session.flush()
        return result
