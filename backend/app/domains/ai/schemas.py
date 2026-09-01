"""AI API schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AIAskRequest(BaseModel):
    message: str = Field(min_length=1, max_length=6000)
    task_type: str = Field(default="career_guidance", min_length=2, max_length=60)


class AIAskResponse(BaseModel):
    interaction_id: uuid.UUID
    answer: str
    provider: str
    model: str
    context_version: str
    disclaimer: str


class AIInteractionRead(BaseModel):
    id: uuid.UUID
    task_type: str
    provider: str
    model: str
    prompt_version: str
    context_version: str
    status: str
    latency_ms: int | None
    error_code: str | None
    created_at: datetime
