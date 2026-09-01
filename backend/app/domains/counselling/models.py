"""Counselling Intelligence domain models.

This domain stores structured guidance sessions and action plans.
It does not contain the future AI counsellor.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CounsellingSession(Base):
    __tablename__ = "counselling_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_type: Mapped[str] = mapped_column(String(60), nullable=False, default="career_guidance")
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="open")
    primary_topic: Mapped[str | None] = mapped_column(String(250), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    notes: Mapped[list["CounsellingNote"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="selectin"
    )
    decisions: Mapped[list["CounsellingDecision"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="selectin"
    )
    action_items: Mapped[list["CounsellingActionItem"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="selectin"
    )


class CounsellingNote(Base):
    __tablename__ = "counselling_notes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("counselling_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    note_type: Mapped[str] = mapped_column(String(50), nullable=False, default="observation")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(40), nullable=False, default="student")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    session: Mapped[CounsellingSession] = relationship(back_populates="notes")


class CounsellingDecision(Base):
    __tablename__ = "counselling_decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("counselling_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    decision_type: Mapped[str] = mapped_column(String(60), nullable=False)
    decision: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    session: Mapped[CounsellingSession] = relationship(back_populates="decisions")


class CounsellingActionItem(Base):
    __tablename__ = "counselling_action_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("counselling_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    action_type: Mapped[str] = mapped_column(String(60), nullable=False, default="general")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="open")
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    session: Mapped[CounsellingSession] = relationship(back_populates="action_items")


class CounsellingGoal(Base):
    __tablename__ = "counselling_goals"
    __table_args__ = (
        UniqueConstraint("student_id", "title", name="uq_counselling_student_goal"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    target_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
