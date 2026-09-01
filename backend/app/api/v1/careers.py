"""Career Intelligence endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.careers.schemas import CareerCandidateRead, CareerDetailRead, CareerRead
from app.domains.careers.service import CareerService

router = APIRouter(prefix="/careers", tags=["Careers"])


@router.get("", response_model=list[CareerRead])
async def list_careers(
    category: str | None = Query(default=None),
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await CareerService(db).list_careers(category)


@router.get("/{career_id}", response_model=CareerDetailRead)
async def get_career(
    career_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await CareerService(db).get_career(career_id)


@router.post("/candidates", response_model=list[CareerCandidateRead])
async def generate_candidates(
    assessment_session_id: UUID | None = Query(default=None),
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await CareerService(db).generate_candidates(user.id, assessment_session_id)
