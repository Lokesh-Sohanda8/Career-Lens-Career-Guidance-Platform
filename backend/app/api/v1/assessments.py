"""Assessment endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.assessments.schemas import (
    AssessmentDetailRead, AssessmentRead, ResponseCreate, ResponseRead,
    ResultRead, SessionRead, SubmitResultRead,
)
from app.domains.assessments.service import AssessmentService
from app.domains.student.service import StudentService

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.get("", response_model=list[AssessmentRead])
async def list_assessments(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await AssessmentService(db).list_active()


@router.get("/{assessment_id}", response_model=AssessmentDetailRead)
async def get_assessment(
    assessment_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    version = await AssessmentService(db).get_detail(assessment_id)
    assessment = version.assessment
    return AssessmentDetailRead(
        id=assessment.id,
        code=assessment.code,
        name=assessment.name,
        description=assessment.description,
        version_id=version.id,
        version=version.version,
        instructions=version.instructions,
        dimensions=version.dimensions,
        questions=version.questions,
    )


@router.post("/{assessment_id}/sessions", response_model=SessionRead, status_code=201)
async def start_assessment(
    assessment_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    student = await StudentService(db).get_for_user(user.id)
    from fastapi import HTTPException
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    return await AssessmentService(db).start(student.id, assessment_id)


@router.post("/sessions/{session_id}/responses", response_model=ResponseRead)
async def save_response(
    session_id: UUID,
    payload: ResponseCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    student = await StudentService(db).get_for_user(user.id)
    from fastapi import HTTPException
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    return await AssessmentService(db).save_response(
        student.id, session_id, payload.question_id, payload.selected_option_id
    )


@router.post("/sessions/{session_id}/complete", response_model=SubmitResultRead)
async def complete_assessment(
    session_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    student = await StudentService(db).get_for_user(user.id)
    from fastapi import HTTPException
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    session, result = await AssessmentService(db).complete(student.id, session_id)
    payload = result.result_payload
    return SubmitResultRead(
        session=session,
        result=ResultRead(
            id=result.id,
            session_id=result.session_id,
            scoring_version=result.scoring_version,
            scores=payload["scores"],
            normalized_traits=payload["normalized_traits"],
            completed_at=result.completed_at,
        ),
    )
