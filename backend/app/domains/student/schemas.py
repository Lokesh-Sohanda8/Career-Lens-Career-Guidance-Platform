"""Student Profile API schemas."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class AcademicRecordCreate(BaseModel):
    subject: str = Field(min_length=1, max_length=100)
    academic_year: str = Field(min_length=1, max_length=20)
    score: int | None = Field(default=None, ge=0, le=100)
    grade: str | None = Field(default=None, max_length=10)
    notes: str | None = None


class AcademicRecordRead(AcademicRecordCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class InterestCreate(BaseModel):
    interest: str = Field(min_length=1, max_length=150)
    level: int | None = Field(default=None, ge=1, le=5)


class InterestRead(InterestCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class PreferenceCreate(BaseModel):
    key: str = Field(min_length=1, max_length=100)
    value: str = Field(min_length=1, max_length=500)


class PreferenceRead(PreferenceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class GoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: int = Field(default=3, ge=1, le=5)
    target_date: date | None = None


class GoalRead(GoalCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class ConstraintCreate(BaseModel):
    key: str = Field(min_length=1, max_length=100)
    value: str = Field(min_length=1, max_length=500)
    importance: int = Field(default=3, ge=1, le=5)


class ConstraintRead(ConstraintCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class StudentCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    date_of_birth: date | None = None
    current_grade: str | None = Field(default=None, max_length=50)
    bio: str | None = None


class StudentUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    date_of_birth: date | None = None
    current_grade: str | None = Field(default=None, max_length=50)
    bio: str | None = None


class StudentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    first_name: str
    last_name: str | None
    date_of_birth: date | None
    current_grade: str | None
    bio: str | None
    created_at: datetime
    updated_at: datetime
    academic_records: list[AcademicRecordRead] = []
    interests: list[InterestRead] = []
    preferences: list[PreferenceRead] = []
    goals: list[GoalRead] = []
    constraints: list[ConstraintRead] = []
