"""Recommendation Engine endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domains.recommendations.schemas import (
    RecommendationFactorRead, RecommendationHistoryRead, RecommendationItemRead,
    RecommendationRead, RecommendationRequest,
)
from app.domains.recommendations.service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def _serialize(run):
    factors = [
        RecommendationFactorRead(
            factor_code=f.factor_code,
            weight=f.weight,
            description=f.description,
        )
        for f in getattr(run, "factors", [])
    ]
    return factors


@router.post("/generate", response_model=RecommendationRead, status_code=201)
async def generate_recommendations(
    payload: RecommendationRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RecommendationService(db)
    run, ranked = await service.generate(
        user.id, payload.assessment_session_id, payload.limit
    )
    factors = []
    for code, weight in service.__class__.__module__ and []:
        pass
    # Re-read the run to load its factor collection for the response.
    run = await service.get(user.id, run.id)
    return RecommendationRead(
        run_id=run.id,
        engine_version=run.engine_version,
        created_at=run.created_at,
        factors=[
            RecommendationFactorRead(
                factor_code=f.factor_code,
                weight=f.weight,
                description=f.description,
            )
            for f in run.factors
        ],
        recommendations=[
            RecommendationItemRead(
                career_id=i.career_id,
                rank=i.rank,
                score=i.score,
                confidence=i.confidence,
                evidence=i.evidence,
                gaps=i.gaps,
                explanation=i.explanation,
            )
            for i in sorted(run.items, key=lambda x: x.rank)
        ],
    )


@router.get("/history", response_model=list[RecommendationHistoryRead])
async def recommendation_history(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = await RecommendationService(db).history(user.id)
    return [
        RecommendationHistoryRead(
            run_id=run.id,
            engine_version=run.engine_version,
            status=run.status,
            created_at=run.created_at,
            recommendation_count=count,
        )
        for run, count in rows
    ]


@router.get("/{run_id}", response_model=RecommendationRead)
async def get_recommendation_run(
    run_id: UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    run = await RecommendationService(db).get(user.id, run_id)
    return RecommendationRead(
        run_id=run.id,
        engine_version=run.engine_version,
        created_at=run.created_at,
        factors=[
            RecommendationFactorRead(
                factor_code=f.factor_code,
                weight=f.weight,
                description=f.description,
            )
            for f in run.factors
        ],
        recommendations=[
            RecommendationItemRead(
                career_id=i.career_id,
                rank=i.rank,
                score=i.score,
                confidence=i.confidence,
                evidence=i.evidence,
                gaps=i.gaps,
                explanation=i.explanation,
            )
            for i in sorted(run.items, key=lambda x: x.rank)
        ],
    )
