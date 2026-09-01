"""Career Intelligence domain SQLAlchemy models."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CareerCategory(Base):
    __tablename__ = "career_categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    careers: Mapped[list["Career"]] = relationship(back_populates="category", lazy="selectin")


class Career(Base):
    __tablename__ = "careers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    work_environment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    education_summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    category: Mapped[CareerCategory | None] = relationship(back_populates="careers", lazy="selectin")
    requirements: Mapped[list["CareerRequirement"]] = relationship(
        back_populates="career", cascade="all, delete-orphan", lazy="selectin"
    )
    education_paths: Mapped[list["CareerEducationPath"]] = relationship(
        back_populates="career", cascade="all, delete-orphan", lazy="selectin"
    )
    skill_requirements: Mapped[list["CareerSkillRequirement"]] = relationship(
        "CareerSkillRequirement", foreign_keys="CareerSkillRequirement.career_id",
        cascade="all, delete-orphan", lazy="selectin"
    )


class CareerRequirement(Base):
    __tablename__ = "career_requirements"
    __table_args__ = (
        UniqueConstraint("career_id", "requirement_type", "name", name="uq_career_requirement"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("careers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    requirement_type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    importance: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    career: Mapped[Career] = relationship(back_populates="requirements")


class CareerEducationPath(Base):
    __tablename__ = "career_education_paths"
    __table_args__ = (
        UniqueConstraint("career_id", "program_name", name="uq_career_education_path"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("careers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    program_name: Mapped[str] = mapped_column(String(250), nullable=False)
    degree_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    subject_area: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    career: Mapped[Career] = relationship(back_populates="education_paths")
