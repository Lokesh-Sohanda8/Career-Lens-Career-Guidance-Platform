"""Persistence operations for the Student Profile domain."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.student.models import (
    AcademicRecord,
    Student,
    StudentConstraint,
    StudentGoal,
    StudentInterest,
    StudentPreference,
)


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: uuid.UUID) -> Student | None:
        result = await self.session.execute(select(Student).where(Student.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_by_id(self, student_id: uuid.UUID) -> Student | None:
        result = await self.session.execute(select(Student).where(Student.id == student_id))
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID, **data) -> Student:
        student = Student(user_id=user_id, **data)
        self.session.add(student)
        await self.session.flush()
        await self.session.refresh(student)
        return student

    async def update(self, student: Student, **data) -> Student:
        for key, value in data.items():
            if value is not None:
                setattr(student, key, value)
        await self.session.flush()
        await self.session.refresh(student)
        return student

    async def add_academic_record(self, student_id: uuid.UUID, **data) -> AcademicRecord:
        record = AcademicRecord(student_id=student_id, **data)
        self.session.add(record)
        await self.session.flush()
        return record

    async def add_interest(self, student_id: uuid.UUID, **data) -> StudentInterest:
        item = StudentInterest(student_id=student_id, **data)
        self.session.add(item)
        await self.session.flush()
        return item

    async def add_preference(self, student_id: uuid.UUID, **data) -> StudentPreference:
        item = StudentPreference(student_id=student_id, **data)
        self.session.add(item)
        await self.session.flush()
        return item

    async def add_goal(self, student_id: uuid.UUID, **data) -> StudentGoal:
        item = StudentGoal(student_id=student_id, **data)
        self.session.add(item)
        await self.session.flush()
        return item

    async def add_constraint(self, student_id: uuid.UUID, **data) -> StudentConstraint:
        item = StudentConstraint(student_id=student_id, **data)
        self.session.add(item)
        await self.session.flush()
        return item
