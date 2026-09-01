"""Learning Intelligence business workflows."""

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.learning.repository import LearningRepository
from app.domains.student.service import StudentService


class LearningService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = LearningRepository(session)
        self.students = StudentService(session)

    async def resources(self, skill_id=None):
        return await self.repo.resources(skill_id)

    async def paths(self, career_id=None):
        return await self.repo.paths(career_id)

    async def path(self, path_id):
        item = await self.repo.path_detail(path_id)
        if not item:
            raise HTTPException(status_code=404, detail="Learning path not found.")
        return item

    async def create_plan(self, user_id, path_id):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")

        path = await self.repo.path_detail(path_id)
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found.")

        existing = await self.repo.get_student_plan(student.id, path_id)
        if existing:
            return existing

        plan = await self.repo.create_plan(student.id, path_id)
        await self.session.commit()
        return plan

    async def update_progress(self, user_id, plan_id, step_id, status, progress_percent):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")

        plan = await self.repo.update_progress(
            student.id, plan_id, step_id, status, progress_percent
        )
        if not plan:
            raise HTTPException(status_code=404, detail="Learning plan or step not found.")

        await self.session.commit()
        return plan
