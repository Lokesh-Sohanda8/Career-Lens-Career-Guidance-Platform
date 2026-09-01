"""Learning Intelligence persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.learning.models import (
    LearningPath, LearningPathStep, LearningResource, StudentLearningPlan,
    StudentLearningProgress,
)


class LearningRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def resources(self, skill_id=None):
        stmt = select(LearningResource).where(LearningResource.is_active.is_(True)).order_by(LearningResource.title)
        if skill_id:
            from app.domains.learning.models import ResourceSkill
            stmt = stmt.join(ResourceSkill).where(ResourceSkill.skill_id == skill_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())

    async def paths(self, career_id=None):
        stmt = (
            select(LearningPath)
            .where(LearningPath.is_active.is_(True))
            .options(selectinload(LearningPath.steps))
            .order_by(LearningPath.title)
        )
        if career_id:
            stmt = stmt.where(LearningPath.target_career_id == career_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())

    async def path_detail(self, path_id):
        result = await self.session.execute(
            select(LearningPath)
            .where(LearningPath.id == path_id, LearningPath.is_active.is_(True))
            .options(selectinload(LearningPath.steps))
        )
        return result.scalar_one_or_none()

    async def get_student_plan(self, student_id, path_id):
        result = await self.session.execute(
            select(StudentLearningPlan)
            .where(
                StudentLearningPlan.student_id == student_id,
                StudentLearningPlan.path_id == path_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_plan(self, student_id, path_id):
        plan = StudentLearningPlan(student_id=student_id, path_id=path_id, status="active", progress_percent=0.0)
        self.session.add(plan)
        await self.session.flush()

        path = await self.path_detail(path_id)
        for step in path.steps:
            self.session.add(
                StudentLearningProgress(
                    plan_id=plan.id,
                    step_id=step.id,
                    status="not_started",
                    progress_percent=0.0,
                )
            )
        return plan

    async def update_progress(self, student_id, plan_id, step_id, status, progress_percent):
        result = await self.session.execute(
            select(StudentLearningPlan)
            .where(
                StudentLearningPlan.id == plan_id,
                StudentLearningPlan.student_id == student_id,
            )
        )
        plan = result.scalar_one_or_none()
        if not plan:
            return None

        progress = await self.session.execute(
            select(StudentLearningProgress)
            .where(
                StudentLearningProgress.plan_id == plan_id,
                StudentLearningProgress.step_id == step_id,
            )
        )
        item = progress.scalar_one_or_none()
        if not item:
            return None

        item.status = status
        item.progress_percent = progress_percent

        all_progress = await self.session.execute(
            select(StudentLearningProgress).where(StudentLearningProgress.plan_id == plan_id)
        )
        rows = list(all_progress.scalars().all())
        plan.progress_percent = round(
            sum(row.progress_percent for row in rows) / len(rows), 2
        ) if rows else 0.0

        if plan.progress_percent >= 100:
            plan.status = "completed"
        elif plan.progress_percent > 0:
            plan.status = "active"

        return plan
