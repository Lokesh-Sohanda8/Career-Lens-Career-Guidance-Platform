"""Learning Intelligence API schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    title: str
    resource_type: str
    provider_name: str | None
    url: str | None
    difficulty: str | None
    estimated_minutes: int | None
    description: str | None


class LearningStepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    skill_id: uuid.UUID | None
    title: str
    description: str | None
    step_order: int
    estimated_minutes: int | None


class LearningPathRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    title: str
    description: str | None
    target_career_id: uuid.UUID | None


class LearningPathDetailRead(LearningPathRead):
    steps: list[LearningStepRead] = []


class LearningPlanCreate(BaseModel):
    path_id: uuid.UUID


class LearningProgressUpdate(BaseModel):
    step_id: uuid.UUID
    status: str = Field(pattern="^(not_started|in_progress|completed)$")
    progress_percent: float = Field(ge=0, le=100)


class LearningPlanRead(BaseModel):
    id: uuid.UUID
    path_id: uuid.UUID
    status: str
    progress_percent: float
    started_at: datetime | None
    completed_at: datetime | None
