"""Counselling Intelligence workflows."""

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.counselling.repository import CounsellingRepository
from app.domains.student.service import StudentService


class CounsellingService:
    def __init__(self, session: AsyncSession):
        self.repo = CounsellingRepository(session)
        self.students = StudentService(session)
        self.session = session

    async def _student(self, user_id):
        student = await self.students.get_for_user(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found.")
        return student

    async def sessions(self, user_id):
        student = await self._student(user_id)
        return await self.repo.sessions(student.id)

    async def create_session(self, user_id, data):
        student = await self._student(user_id)
        item = await self.repo.create_session(student.id, data)
        await self.session.commit()
        return item

    async def update_session(self, user_id, session_id, data):
        student = await self._student(user_id)
        item = await self.repo.session(student.id, session_id)
        if not item:
            raise HTTPException(status_code=404, detail="Counselling session not found.")
        for key, value in data.model_dump().items():
            setattr(item, key, value)
        await self.session.commit()
        return item

    async def add_note(self, user_id, session_id, data):
        student = await self._student(user_id)
        item = await self.repo.add_note(student.id, session_id, data)
        if not item:
            raise HTTPException(status_code=404, detail="Counselling session not found.")
        await self.session.commit()
        return item

    async def add_decision(self, user_id, session_id, data):
        student = await self._student(user_id)
        item = await self.repo.add_decision(student.id, session_id, data)
        if not item:
            raise HTTPException(status_code=404, detail="Counselling session not found.")
        await self.session.commit()
        return item

    async def add_action_item(self, user_id, session_id, data):
        student = await self._student(user_id)
        item = await self.repo.add_action_item(student.id, session_id, data)
        if not item:
            raise HTTPException(status_code=404, detail="Counselling session not found.")
        await self.session.commit()
        return item

    async def update_action_item(self, user_id, action_id, data):
        student = await self._student(user_id)
        item = await self.repo.update_action_item(student.id, action_id, data.status)
        if not item:
            raise HTTPException(status_code=404, detail="Action item not found.")
        await self.session.commit()
        return item

    async def goals(self, user_id):
        student = await self._student(user_id)
        return await self.repo.goals(student.id)

    async def create_goal(self, user_id, data):
        student = await self._student(user_id)
        item = await self.repo.create_goal(student.id, data)
        await self.session.commit()
        return item

    async def update_goal(self, user_id, goal_id, data):
        student = await self._student(user_id)
        item = await self.repo.update_goal(student.id, goal_id, data.status)
        if not item:
            raise HTTPException(status_code=404, detail="Counselling goal not found.")
        await self.session.commit()
        return item
