"""Assessment domain SQLAlchemy models."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    versions: Mapped[list["AssessmentVersion"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan", lazy="selectin"
    )


class AssessmentVersion(Base):
    __tablename__ = "assessment_versions"
    __table_args__ = (UniqueConstraint("assessment_id", "version", name="uq_assessment_version"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    scoring_version: Mapped[str] = mapped_column(String(50), default="v1", nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    assessment: Mapped[Assessment] = relationship(back_populates="versions")
    dimensions: Mapped[list["AssessmentDimension"]] = relationship(
        back_populates="version", cascade="all, delete-orphan", lazy="selectin"
    )
    questions: Mapped[list["AssessmentQuestion"]] = relationship(
        back_populates="version", cascade="all, delete-orphan", lazy="selectin"
    )


class AssessmentDimension(Base):
    __tablename__ = "assessment_dimensions"
    __table_args__ = (UniqueConstraint("assessment_version_id", "code", name="uq_assessment_dimension_code"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    version: Mapped[AssessmentVersion] = relationship(back_populates="dimensions")


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"
    __table_args__ = (UniqueConstraint("assessment_version_id", "question_number", name="uq_assessment_question_number"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dimension_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_dimensions.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    question_number: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(50), default="single_choice", nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    version: Mapped[AssessmentVersion] = relationship(back_populates="questions")
    dimension: Mapped[AssessmentDimension] = relationship()
    options: Mapped[list["AssessmentOption"]] = relationship(
        back_populates="question", cascade="all, delete-orphan", lazy="selectin"
    )


class AssessmentOption(Base):
    __tablename__ = "assessment_options"
    __table_args__ = (UniqueConstraint("question_id", "option_number", name="uq_assessment_option_number"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    option_number: Mapped[int] = mapped_column(Integer, nullable=False)
    label: Mapped[str] = mapped_column(String(500), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    question: Mapped[AssessmentQuestion] = relationship(back_populates="options")


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_versions.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(30), default="in_progress", nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    responses: Mapped[list["AssessmentResponse"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="selectin"
    )
    result: Mapped["AssessmentResult | None"] = relationship(
        back_populates="session", cascade="all, delete-orphan", uselist=False, lazy="selectin"
    )


class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"
    __table_args__ = (UniqueConstraint("session_id", "question_id", name="uq_assessment_response_question"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_questions.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    selected_option_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_options.id", ondelete="RESTRICT"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    session: Mapped[AssessmentSession] = relationship(back_populates="responses")


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessment_sessions.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    scoring_version: Mapped[str] = mapped_column(String(50), nullable=False)
    result_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    session: Mapped[AssessmentSession] = relationship(back_populates="result")
