"""Persistence operations for Skill Intelligence."""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.domains.skills.models import CareerSkillRequirement, Skill, SkillCategory, StudentSkillEvidence
class SkillRepository:
    def __init__(self, session: AsyncSession): self.session=session
    async def list_active(self, category_code=None):
        stmt=select(Skill).where(Skill.is_active.is_(True)).options(selectinload(Skill.category)).order_by(Skill.name)
        if category_code: stmt=stmt.join(SkillCategory).where(SkillCategory.code==category_code)
        return list((await self.session.execute(stmt)).scalars().all())
    async def get_skill(self, skill_id):
        r=await self.session.execute(select(Skill).where(Skill.id==skill_id, Skill.is_active.is_(True)).options(selectinload(Skill.category))); return r.scalar_one_or_none()
    async def get_evidence(self, student_id):
        r=await self.session.execute(select(StudentSkillEvidence).where(StudentSkillEvidence.student_id==student_id).options(selectinload(StudentSkillEvidence.skill)).order_by(StudentSkillEvidence.updated_at.desc())); return list(r.scalars().all())
    async def upsert_evidence(self, student_id, skill_id, **data):
        r=await self.session.execute(select(StudentSkillEvidence).where(StudentSkillEvidence.student_id==student_id, StudentSkillEvidence.skill_id==skill_id)); item=r.scalar_one_or_none()
        if item:
            for k,v in data.items(): setattr(item,k,v)
        else:
            item=StudentSkillEvidence(student_id=student_id, skill_id=skill_id, **data); self.session.add(item)
        await self.session.flush(); return item
    async def career_requirements(self, career_id):
        r=await self.session.execute(select(CareerSkillRequirement).where(CareerSkillRequirement.career_id==career_id).options(selectinload(CareerSkillRequirement.skill)).order_by(CareerSkillRequirement.importance.desc(), CareerSkillRequirement.required_level.desc())); return list(r.scalars().all())
