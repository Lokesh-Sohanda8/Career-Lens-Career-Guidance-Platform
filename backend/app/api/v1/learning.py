"""Learning Intelligence endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.learning.schemas import (
    LearningPathDetailRead, LearningPathRead, LearningPlanCreate,
    LearningPlanRead, LearningProgressUpdate, ResourceRead,
)
from app.domains.learning.service import LearningService

router = APIRouter(prefix="/learning", tags=["Learning"])


@router.get("/resources", response_model=list[ResourceRead])
async def list_resources(
    skill_id: UUID | None = Query(default=None),
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await LearningService(db).resources(skill_id)


@router.get("/paths", response_model=list[LearningPathRead])
async def list_paths(
    career_id: UUID | None = Query(default=None),
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await LearningService(db).paths(career_id)


@router.get("/paths/{path_id}", response_model=LearningPathDetailRead)
async def get_path(
    path_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await LearningService(db).path(path_id)


@router.post("/plans", response_model=LearningPlanRead, status_code=201)
async def create_plan(
    payload: LearningPlanCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await LearningService(db).create_plan(user.id, payload.path_id)


@router.patch("/plans/{plan_id}/progress", response_model=LearningPlanRead)
async def update_progress(
    plan_id: UUID,
    payload: LearningProgressUpdate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await LearningService(db).update_progress(
        user.id,
        plan_id,
        payload.step_id,
        payload.status,
        payload.progress_percent,
    )
