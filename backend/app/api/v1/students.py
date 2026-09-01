"""Student Profile endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.student.schemas import (
    AcademicRecordCreate, AcademicRecordRead, ConstraintCreate, ConstraintRead,
    GoalCreate, GoalRead, InterestCreate, InterestRead, PreferenceCreate,
    PreferenceRead, StudentCreate, StudentRead, StudentUpdate,
)
from app.domains.student.service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/me", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_profile(
    payload: StudentCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await StudentService(db).create_profile(user.id, **payload.model_dump())


@router.get("/me", response_model=StudentRead)
async def get_profile(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from fastapi import HTTPException
    student = await StudentService(db).get_for_user(user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    return student


@router.patch("/me", response_model=StudentRead)
async def update_profile(
    payload: StudentUpdate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await StudentService(db).update_profile(
        user.id, **payload.model_dump(exclude_unset=True)
    )


@router.post("/me/academic-records", response_model=AcademicRecordRead, status_code=201)
async def add_academic_record(
    payload: AcademicRecordCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await StudentService(db).add_academic_record(user.id, **payload.model_dump())


@router.post("/me/interests", response_model=InterestRead, status_code=201)
async def add_interest(
    payload: InterestCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await StudentService(db).add_interest(user.id, **payload.model_dump())


@router.post("/me/preferences", response_model=PreferenceRead, status_code=201)
async def add_preference(
    payload: PreferenceCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await StudentService(db).add_preference(user.id, **payload.model_dump())


@router.post("/me/goals", response_model=GoalRead, status_code=201)
async def add_goal(
    payload: GoalCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await StudentService(db).add_goal(user.id, **payload.model_dump())


@router.post("/me/constraints", response_model=ConstraintRead, status_code=201)
async def add_constraint(
    payload: ConstraintCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await StudentService(db).add_constraint(user.id, **payload.model_dump())
