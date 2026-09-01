"""Counselling persistence operations."""

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.counselling.models import (
    CounsellingActionItem, CounsellingDecision, CounsellingGoal,
    CounsellingNote, CounsellingSession,
)


class CounsellingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def sessions(self, student_id):
        result = await self.session.execute(
            select(CounsellingSession)
            .where(CounsellingSession.student_id == student_id)
            .order_by(CounsellingSession.created_at.desc())
        )
        return list(result.scalars().all())

    async def session(self, student_id, session_id):
        result = await self.session.execute(
            select(CounsellingSession)
            .where(
                CounsellingSession.id == session_id,
                CounsellingSession.student_id == student_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_session(self, student_id, data):
        item = CounsellingSession(student_id=student_id, **data.model_dump())
        self.session.add(item)
        await self.session.flush()
        return item

    async def add_note(self, student_id, session_id, data):
        session = await self.session(student_id, session_id)
        if not session:
            return None
        item = CounsellingNote(session_id=session_id, **data.model_dump())
        self.session.add(item)
        return item

    async def add_decision(self, student_id, session_id, data):
        session = await self.session(student_id, session_id)
        if not session:
            return None
        item = CounsellingDecision(session_id=session_id, **data.model_dump())
        self.session.add(item)
        return item

    async def add_action_item(self, student_id, session_id, data):
        session = await self.session(student_id, session_id)
        if not session:
            return None
        item = CounsellingActionItem(session_id=session_id, **data.model_dump())
        self.session.add(item)
        return item

    async def update_action_item(self, student_id, action_id, status):
        result = await self.session.execute(
            select(CounsellingActionItem)
            .join(CounsellingSession)
            .where(
                CounsellingActionItem.id == action_id,
                CounsellingSession.student_id == student_id,
            )
        )
        item = result.scalar_one_or_none()
        if not item:
            return None
        item.status = status
        if status == "completed":
            item.completed_at = datetime.utcnow()
        else:
            item.completed_at = None
        return item

    async def goals(self, student_id):
        result = await self.session.execute(
            select(CounsellingGoal)
            .where(CounsellingGoal.student_id == student_id)
            .order_by(CounsellingGoal.priority.desc(), CounsellingGoal.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_goal(self, student_id, data):
        item = CounsellingGoal(student_id=student_id, **data.model_dump())
        self.session.add(item)
        await self.session.flush()
        return item

    async def update_goal(self, student_id, goal_id, status):
        result = await self.session.execute(
            select(CounsellingGoal)
            .where(
                CounsellingGoal.id == goal_id,
                CounsellingGoal.student_id == student_id,
            )
        )
        item = result.scalar_one_or_none()
        if not item:
            return None
        item.status = status
        return item
