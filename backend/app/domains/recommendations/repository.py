"""Recommendation persistence operations."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.recommendations.models import RecommendationFactor, RecommendationItem, RecommendationRun


class RecommendationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_run(self, student_id, assessment_session_id, engine_version):
        run = RecommendationRun(
            student_id=student_id,
            assessment_session_id=assessment_session_id,
            engine_version=engine_version,
            status="completed",
        )
        self.session.add(run)
        await self.session.flush()
        return run

    async def add_factor(self, run_id, code, weight, description):
        self.session.add(
            RecommendationFactor(
                run_id=run_id, factor_code=code, weight=weight, description=description
            )
        )

    async def add_item(self, run_id, item):
        self.session.add(
            RecommendationItem(
                run_id=run_id,
                career_id=item["career_id"],
                rank=item["rank"],
                score=item["score"],
                confidence=item["confidence"],
                evidence=item["evidence"],
                gaps=item["gaps"],
                explanation=item["explanation"],
            )
        )

    async def get_run(self, run_id, student_id):
        result = await self.session.execute(
            select(RecommendationRun)
            .where(
                RecommendationRun.id == run_id,
                RecommendationRun.student_id == student_id,
            )
            .options(
                selectinload(RecommendationRun.items),
            )
        )
        return result.scalar_one_or_none()

    async def history(self, student_id):
        result = await self.session.execute(
            select(
                RecommendationRun,
                func.count(RecommendationItem.id).label("item_count"),
            )
            .outerjoin(RecommendationItem, RecommendationItem.run_id == RecommendationRun.id)
            .where(RecommendationRun.student_id == student_id)
            .group_by(RecommendationRun.id)
            .order_by(RecommendationRun.created_at.desc())
        )
        return list(result.all())
