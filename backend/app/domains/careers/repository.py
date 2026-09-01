"""Persistence operations for Career Intelligence."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.careers.models import Career, CareerCategory


class CareerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_active(self, category_code: str | None = None):
        stmt = (
            select(Career)
            .where(Career.is_active.is_(True))
            .options(selectinload(Career.category))
            .order_by(Career.title)
        )
        if category_code:
            stmt = stmt.join(CareerCategory).where(CareerCategory.code == category_code)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_detail(self, career_id: uuid.UUID):
        result = await self.session.execute(
            select(Career)
            .where(Career.id == career_id, Career.is_active.is_(True))
            .options(
                selectinload(Career.category),
                selectinload(Career.requirements),
                selectinload(Career.education_paths),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_codes(self, codes: list[str]):
        if not codes:
            return []
        result = await self.session.execute(
            select(Career)
            .where(Career.code.in_(codes), Career.is_active.is_(True))
            .options(selectinload(Career.category), selectinload(Career.requirements))
        )
        return list(result.scalars().all())
