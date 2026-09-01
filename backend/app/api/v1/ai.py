"""AI assistance endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.ai.schemas import AIAskRequest, AIAskResponse, AIInteractionRead
from app.domains.ai.repository import AIRepository
from app.domains.ai.service import AIService
from app.domains.student.service import StudentService

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/ask", response_model=AIAskResponse)
async def ask_ai(
    payload: AIAskRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    interaction, result = await AIService(db).ask(
        user.id, payload.message, payload.task_type
    )
    return AIAskResponse(
        interaction_id=interaction.id,
        answer=result.text,
        provider=result.provider,
        model=result.model,
        context_version=interaction.context_version,
        disclaimer=(
            "AI guidance is decision support, not a guarantee. "
            "Verify important education or admission requirements with official sources."
        ),
    )


@router.get("/interactions", response_model=list[AIInteractionRead])
async def list_ai_interactions(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    student = await StudentService(db).get_for_user(user.id)
    if not student:
        return []
    return await AIRepository(db).list_for_student(student.id)
