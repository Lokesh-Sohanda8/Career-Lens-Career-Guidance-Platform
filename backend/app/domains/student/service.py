"""Business logic for the Student Profile domain."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.student.repository import StudentRepository


class StudentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = StudentRepository(session)

    async def get_for_user(self, user_id: uuid.UUID):
        return await self.repo.get_by_user_id(user_id)

    async def create_profile(self, user_id: uuid.UUID, **data):
        if await self.repo.get_by_user_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A student profile already exists for this user.",
            )
        try:
            student = await self.repo.create(user_id, **data)
            await self.session.commit()
            await self.session.refresh(student)
            return student
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Could not create the student profile.",
            ) from None

    async def update_profile(self, user_id: uuid.UUID, **data):
        student = await self.repo.get_by_user_id(user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found.",
            )
        student = await self.repo.update(student, **data)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    async def add_academic_record(self, user_id: uuid.UUID, **data):
        student = await self._require(user_id)
        try:
            item = await self.repo.add_academic_record(student.id, **data)
            await self.session.commit()
            return item
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This academic record already exists.",
            ) from None

    async def add_interest(self, user_id: uuid.UUID, **data):
        student = await self._require(user_id)
        try:
            item = await self.repo.add_interest(student.id, **data)
            await self.session.commit()
            return item
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This interest is already recorded.",
            ) from None

    async def add_preference(self, user_id: uuid.UUID, **data):
        student = await self._require(user_id)
        try:
            item = await self.repo.add_preference(student.id, **data)
            await self.session.commit()
            return item
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This preference already exists.",
            ) from None

    async def add_goal(self, user_id: uuid.UUID, **data):
        student = await self._require(user_id)
        item = await self.repo.add_goal(student.id, **data)
        await self.session.commit()
        return item

    async def add_constraint(self, user_id: uuid.UUID, **data):
        student = await self._require(user_id)
        item = await self.repo.add_constraint(student.id, **data)
        await self.session.commit()
        return item

    async def _require(self, user_id: uuid.UUID):
        student = await self.repo.get_by_user_id(user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found.",
            )
        return student
