"""Skill Intelligence business logic."""
import uuid
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.skills.repository import SkillRepository
from app.domains.skills.gap_analysis import SkillGapAnalyzer
from app.domains.student.service import StudentService
class SkillService:
    def __init__(self,session): self.session=session; self.repo=SkillRepository(session); self.students=StudentService(session)
    async def list_skills(self,category_code=None): return await self.repo.list_active(category_code)
    async def get_skill(self,skill_id):
        item=await self.repo.get_skill(skill_id)
        if not item: raise HTTPException(404,"Skill not found.")
        return item
    async def upsert_evidence(self,user_id,**data):
        student=await self.students.get_for_user(user_id)
        if not student: raise HTTPException(404,"Student profile not found.")
        if not await self.repo.get_skill(data["skill_id"]): raise HTTPException(404,"Skill not found.")
        item=await self.repo.upsert_evidence(student.id,**data); await self.session.commit(); await self.session.refresh(item); return item
    async def list_evidence(self,user_id):
        student=await self.students.get_for_user(user_id)
        if not student: raise HTTPException(404,"Student profile not found.")
        return await self.repo.get_evidence(student.id)
    async def skill_gaps(self,user_id,career_id):
        student=await self.students.get_for_user(user_id)
        if not student: raise HTTPException(404,"Student profile not found.")
        reqs=await self.repo.career_requirements(career_id)
        if not reqs: raise HTTPException(404,"No skill requirements found for this career.")
        return SkillGapAnalyzer.analyze(reqs,await self.repo.get_evidence(student.id))
