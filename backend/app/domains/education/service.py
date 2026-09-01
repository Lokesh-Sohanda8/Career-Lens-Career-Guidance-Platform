"""Education Intelligence business workflows."""

import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.education.matching import EducationMatcherV1
from app.domains.education.repository import EducationRepository
from app.domains.student.service import StudentService


class EducationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = EducationRepository(session)
        self.students = StudentService(session)

    async def institutions(self):
        return await self.repo.institutions()

    async def exams(self):
        return await self.repo.exams()

    async def programs(self, career_id=None):
        return await self.repo.programs(career_id)

    async def program(self, program_id):
        item = await self.repo.program_detail(program_id)
        if not item:
            raise HTTPException(status_code=404, detail="Education program not found.")
        return item

    async def match_for_career(self, user_id, career_id):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")

        links = await self.repo.career_programs(career_id)
        if not links:
            raise HTTPException(
                status_code=404,
                detail="No education programs are linked to this career.",
            )

        return EducationMatcherV1.match(student, links)
