"""Education Intelligence persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.education.models import (
    CareerEducationProgram,
    EducationExam,
    EducationInstitution,
    EducationProgram,
)


class EducationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def institutions(self):
        result = await self.session.execute(
            select(EducationInstitution)
            .where(EducationInstitution.is_active.is_(True))
            .order_by(EducationInstitution.name)
        )
        return list(result.scalars().all())

    async def exams(self):
        result = await self.session.execute(
            select(EducationExam)
            .where(EducationExam.is_active.is_(True))
            .order_by(EducationExam.name)
        )
        return list(result.scalars().all())

    async def programs(self, career_id: uuid.UUID | None = None):
        stmt = (
            select(EducationProgram)
            .where(EducationProgram.is_active.is_(True))
            .options(selectinload(EducationProgram.institution))
            .order_by(EducationProgram.name)
        )
        if career_id:
            stmt = (
                stmt.join(CareerEducationProgram)
                .where(CareerEducationProgram.career_id == career_id)
            )
        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())

    async def program_detail(self, program_id: uuid.UUID):
        result = await self.session.execute(
            select(EducationProgram)
            .where(
                EducationProgram.id == program_id,
                EducationProgram.is_active.is_(True),
            )
            .options(
                selectinload(EducationProgram.institution),
                selectinload(EducationProgram.exam_requirements).selectinload(
                    "exam"
                ),
                selectinload(EducationProgram.eligibility_rules),
            )
        )
        return result.scalar_one_or_none()

    async def career_programs(self, career_id: uuid.UUID):
        result = await self.session.execute(
            select(CareerEducationProgram)
            .where(CareerEducationProgram.career_id == career_id)
            .options(
                selectinload(CareerEducationProgram.program)
                .selectinload(EducationProgram.institution),
                selectinload(CareerEducationProgram.program)
                .selectinload(EducationProgram.eligibility_rules),
            )
        )
        return list(result.scalars().unique().all())
