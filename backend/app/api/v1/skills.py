"""Skill Intelligence endpoints."""
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.skills.schemas import SkillEvidenceUpsert, SkillGapRead, SkillRead, StudentSkillEvidenceRead
from app.domains.skills.service import SkillService
router=APIRouter(prefix="/skills",tags=["Skills"])
@router.get("",response_model=list[SkillRead])
async def list_skills(category: str|None=Query(default=None), user=Depends(get_current_user), db:AsyncSession=Depends(get_db)): return await SkillService(db).list_skills(category)
@router.get("/{skill_id}",response_model=SkillRead)
async def get_skill(skill_id:UUID,user=Depends(get_current_user),db:AsyncSession=Depends(get_db)): return await SkillService(db).get_skill(skill_id)
@router.get("/me/evidence",response_model=list[StudentSkillEvidenceRead])
async def list_my_skill_evidence(user=Depends(get_current_user),db:AsyncSession=Depends(get_db)): return await SkillService(db).list_evidence(user.id)
@router.put("/me/evidence",response_model=StudentSkillEvidenceRead)
async def upsert_my_skill_evidence(payload:SkillEvidenceUpsert,user=Depends(get_current_user),db:AsyncSession=Depends(get_db)): return await SkillService(db).upsert_evidence(user.id,**payload.model_dump())
@router.get("/me/gaps/{career_id}",response_model=list[SkillGapRead])
async def get_my_skill_gaps(career_id:UUID,user=Depends(get_current_user),db:AsyncSession=Depends(get_db)): return await SkillService(db).skill_gaps(user.id,career_id)
