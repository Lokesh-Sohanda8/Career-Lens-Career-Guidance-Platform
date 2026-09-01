"""AI interaction persistence."""

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.ai.models import AIInteraction


class AIRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs):
        item = AIInteraction(**kwargs)
        self.session.add(item)
        await self.session.flush()
        return item

    async def list_for_student(self, student_id, limit=50):
        result = await self.session.execute(
            select(AIInteraction)
            .where(AIInteraction.student_id == student_id)
            .order_by(AIInteraction.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
