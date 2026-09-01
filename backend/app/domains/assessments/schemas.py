"""Assessment API schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssessmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    description: str | None
    is_active: bool


class AssessmentOptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    option_number: int
    label: str


class AssessmentQuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question_number: int
    text: str
    question_type: str
    is_required: bool
    options: list[AssessmentOptionRead] = []


class AssessmentDimensionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    description: str | None


class AssessmentDetailRead(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    description: str | None
    version_id: uuid.UUID
    version: int
    instructions: str | None
    dimensions: list[AssessmentDimensionRead] = []
    questions: list[AssessmentQuestionRead] = []


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    assessment_version_id: uuid.UUID
    status: str
    started_at: datetime
    completed_at: datetime | None


class ResponseCreate(BaseModel):
    question_id: uuid.UUID
    selected_option_id: uuid.UUID


class ResponseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question_id: uuid.UUID
    selected_option_id: uuid.UUID
    created_at: datetime


class ResultRead(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    scoring_version: str
    scores: dict[str, float]
    normalized_traits: dict[str, float]
    completed_at: datetime


class SubmitResultRead(BaseModel):
    session: SessionRead
    result: ResultRead
