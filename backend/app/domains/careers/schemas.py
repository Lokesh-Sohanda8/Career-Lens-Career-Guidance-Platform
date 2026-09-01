"""Career Intelligence API schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CareerCategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    description: str | None


class CareerRequirementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    requirement_type: str
    name: str
    importance: int
    description: str | None


class CareerEducationPathRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    program_name: str
    degree_level: str | None
    subject_area: str | None
    notes: str | None


class CareerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    title: str
    description: str | None
    work_environment: str | None
    education_summary: str | None
    is_active: bool
    category: CareerCategoryRead | None


class CareerDetailRead(CareerRead):
    requirements: list[CareerRequirementRead] = []
    education_paths: list[CareerEducationPathRead] = []


class CareerCandidateRead(BaseModel):
    career_id: uuid.UUID
    title: str
    category: str | None
    evidence: list[str]
    preliminary_score: float
