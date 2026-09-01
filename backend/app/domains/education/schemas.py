"""Education Intelligence API schemas."""

import uuid

from pydantic import BaseModel, ConfigDict


class InstitutionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    institution_type: str
    country: str
    state: str | None
    city: str | None
    website: str | None


class ExamRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    description: str | None


class EligibilityRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    rule_type: str
    subject: str | None
    minimum_score: float | None
    minimum_percentage: float | None
    value: str | None
    importance: int
    notes: str | None


class ExamRequirementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    required: bool
    minimum_score: float | None
    notes: str | None
    exam: ExamRead


class ProgramSummaryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    name: str
    degree_level: str
    field_of_study: str | None
    duration_months: int | None
    delivery_mode: str | None
    institution: InstitutionRead


class ProgramDetailRead(ProgramSummaryRead):
    exam_requirements: list[ExamRequirementRead] = []
    eligibility_rules: list[EligibilityRuleRead] = []


class EducationMatchRead(BaseModel):
    program_id: uuid.UUID
    program_name: str
    institution_name: str
    career_id: uuid.UUID
    relevance: int
    match_score: float
    status: str
    reasons: list[str]
    unmet_rules: list[str]
