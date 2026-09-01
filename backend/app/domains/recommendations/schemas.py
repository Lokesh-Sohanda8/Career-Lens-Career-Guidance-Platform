"""Recommendation API schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    assessment_session_id: uuid.UUID | None = None
    limit: int = Field(default=5, ge=1, le=20)


class RecommendationEvidence(BaseModel):
    factor: str
    detail: str


class RecommendationItemRead(BaseModel):
    career_id: uuid.UUID
    rank: int
    score: float
    confidence: float
    evidence: list[RecommendationEvidence]
    gaps: list[str]
    explanation: str


class RecommendationFactorRead(BaseModel):
    factor_code: str
    weight: float
    description: str


class RecommendationRead(BaseModel):
    run_id: uuid.UUID
    engine_version: str
    created_at: datetime
    factors: list[RecommendationFactorRead]
    recommendations: list[RecommendationItemRead]


class RecommendationHistoryRead(BaseModel):
    run_id: uuid.UUID
    engine_version: str
    status: str
    created_at: datetime
    recommendation_count: int
