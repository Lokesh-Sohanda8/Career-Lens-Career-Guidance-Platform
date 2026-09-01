"""Education Intelligence domain models.

Education owns institutions, programs, exams, eligibility rules, and
career-to-program relationships.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EducationInstitution(Base):
    __tablename__ = "education_institutions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    institution_type: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="India")
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    programs: Mapped[list["EducationProgram"]] = relationship(
        back_populates="institution", cascade="all, delete-orphan", lazy="selectin"
    )


class EducationProgram(Base):
    __tablename__ = "education_programs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("education_institutions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    degree_level: Mapped[str] = mapped_column(String(100), nullable=False)
    field_of_study: Mapped[str | None] = mapped_column(String(200), nullable=True)
    duration_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    delivery_mode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    institution: Mapped[EducationInstitution] = relationship(back_populates="programs")
    exam_requirements: Mapped[list["ProgramExamRequirement"]] = relationship(
        back_populates="program", cascade="all, delete-orphan", lazy="selectin"
    )
    eligibility_rules: Mapped[list["ProgramEligibilityRule"]] = relationship(
        back_populates="program", cascade="all, delete-orphan", lazy="selectin"
    )
    career_links: Mapped[list["CareerEducationProgram"]] = relationship(
        back_populates="program", cascade="all, delete-orphan", lazy="selectin"
    )


class EducationExam(Base):
    __tablename__ = "education_exams"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class ProgramExamRequirement(Base):
    __tablename__ = "program_exam_requirements"
    __table_args__ = (
        UniqueConstraint("program_id", "exam_id", name="uq_program_exam_requirement"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("education_programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exam_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("education_exams.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    minimum_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    program: Mapped[EducationProgram] = relationship(back_populates="exam_requirements")
    exam: Mapped[EducationExam] = relationship(lazy="selectin")


class ProgramEligibilityRule(Base):
    __tablename__ = "program_eligibility_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("education_programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    rule_type: Mapped[str] = mapped_column(String(80), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(120), nullable=True)
    minimum_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    minimum_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)
    value: Mapped[str | None] = mapped_column(String(300), nullable=True)
    importance: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    program: Mapped[EducationProgram] = relationship(back_populates="eligibility_rules")


class CareerEducationProgram(Base):
    __tablename__ = "career_education_programs"
    __table_args__ = (
        UniqueConstraint("career_id", "program_id", name="uq_career_education_program"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("careers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    program_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("education_programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relevance: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    program: Mapped[EducationProgram] = relationship(back_populates="career_links")
