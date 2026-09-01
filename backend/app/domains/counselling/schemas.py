"""Counselling Intelligence schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    session_type: str = Field(default="career_guidance", min_length=2, max_length=60)
    primary_topic: str | None = Field(default=None, max_length=250)


class SessionUpdate(BaseModel):
    status: str = Field(pattern="^(open|in_progress|closed)$")
    summary: str | None = None


class NoteCreate(BaseModel):
    note_type: str = Field(default="observation", min_length=2, max_length=50)
    content: str = Field(min_length=1)
    source: str = Field(default="student", min_length=2, max_length=40)


class DecisionCreate(BaseModel):
    decision_type: str = Field(min_length=2, max_length=60)
    decision: str = Field(min_length=1)
    rationale: str | None = None
    confidence: str | None = Field(default=None, max_length=30)


class ActionItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    action_type: str = Field(default="general", min_length=2, max_length=60)
    priority: int = Field(default=3, ge=1, le=5)
    due_date: datetime | None = None


class ActionItemUpdate(BaseModel):
    status: str = Field(pattern="^(open|in_progress|completed|cancelled)$")


class GoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=250)
    description: str | None = None
    priority: int = Field(default=3, ge=1, le=5)
    target_date: datetime | None = None


class GoalUpdate(BaseModel):
    status: str = Field(pattern="^(active|completed|paused|cancelled)$")


class SessionRead(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    session_type: str
    status: str
    primary_topic: str | None
    summary: str | None
    created_at: datetime
    updated_at: datetime


class NoteRead(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    note_type: str
    content: str
    source: str
    created_at: datetime


class DecisionRead(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    decision_type: str
    decision: str
    rationale: str | None
    confidence: str | None
    created_at: datetime


class ActionItemRead(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    title: str
    description: str | None
    action_type: str
    priority: int
    status: str
    due_date: datetime | None
    completed_at: datetime | None
    created_at: datetime


class GoalRead(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    title: str
    description: str | None
    status: str
    priority: int
    target_date: datetime | None
    created_at: datetime
    updated_at: datetime
