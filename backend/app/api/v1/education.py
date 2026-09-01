"""Education Intelligence endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.education.schemas import (
    EducationMatchRead,
    ExamRead,
    InstitutionRead,
    ProgramDetailRead,
    ProgramSummaryRead,
)
from app.domains.education.service import EducationService

router = APIRouter(prefix="/education", tags=["Education"])


@router.get("/institutions", response_model=list[InstitutionRead])
async def list_institutions(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await EducationService(db).institutions()


@router.get("/exams", response_model=list[ExamRead])
async def list_exams(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await EducationService(db).exams()


@router.get("/programs", response_model=list[ProgramSummaryRead])
async def list_programs(
    career_id: UUID | None = Query(default=None),
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await EducationService(db).programs(career_id)


@router.get("/programs/{program_id}", response_model=ProgramDetailRead)
async def get_program(
    program_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await EducationService(db).program(program_id)


@router.get("/matches/{career_id}", response_model=list[EducationMatchRead])
async def match_education(
    career_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await EducationService(db).match_for_career(user.id, career_id)
