"""Create Education Intelligence tables.

Revision ID: 20260901_0007
Revises: 20260901_0006
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0007"
down_revision = "20260901_0006"
branch_labels = None
depends_on = None
uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "education_institutions",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(250), nullable=False),
        sa.Column("institution_type", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_education_institutions_code", "education_institutions", ["code"])

    op.create_table(
        "education_programs",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("institution_id", uuid, sa.ForeignKey("education_institutions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(150), nullable=False),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("degree_level", sa.String(100), nullable=False),
        sa.Column("field_of_study", sa.String(200), nullable=True),
        sa.Column("duration_months", sa.Integer(), nullable=True),
        sa.Column("delivery_mode", sa.String(50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_education_programs_institution_id", "education_programs", ["institution_id"])
    op.create_index("ix_education_programs_code", "education_programs", ["code"])

    op.create_table(
        "education_exams",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(250), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_education_exams_code", "education_exams", ["code"])

    op.create_table(
        "program_exam_requirements",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("program_id", uuid, sa.ForeignKey("education_programs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("exam_id", uuid, sa.ForeignKey("education_exams.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("minimum_score", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.UniqueConstraint("program_id", "exam_id", name="uq_program_exam_requirement"),
    )
    op.create_index("ix_program_exam_requirements_program_id", "program_exam_requirements", ["program_id"])
    op.create_index("ix_program_exam_requirements_exam_id", "program_exam_requirements", ["exam_id"])

    op.create_table(
        "program_eligibility_rules",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("program_id", uuid, sa.ForeignKey("education_programs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_type", sa.String(80), nullable=False),
        sa.Column("subject", sa.String(120), nullable=True),
        sa.Column("minimum_score", sa.Float(), nullable=True),
        sa.Column("minimum_percentage", sa.Float(), nullable=True),
        sa.Column("value", sa.String(300), nullable=True),
        sa.Column("importance", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index("ix_program_eligibility_rules_program_id", "program_eligibility_rules", ["program_id"])

    op.create_table(
        "career_education_programs",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("career_id", uuid, sa.ForeignKey("careers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("program_id", uuid, sa.ForeignKey("education_programs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relevance", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.UniqueConstraint("career_id", "program_id", name="uq_career_education_program"),
    )
    op.create_index("ix_career_education_programs_career_id", "career_education_programs", ["career_id"])
    op.create_index("ix_career_education_programs_program_id", "career_education_programs", ["program_id"])


def downgrade() -> None:
    op.drop_index("ix_career_education_programs_program_id", table_name="career_education_programs")
    op.drop_index("ix_career_education_programs_career_id", table_name="career_education_programs")
    op.drop_table("career_education_programs")
    op.drop_index("ix_program_eligibility_rules_program_id", table_name="program_eligibility_rules")
    op.drop_table("program_eligibility_rules")
    op.drop_index("ix_program_exam_requirements_exam_id", table_name="program_exam_requirements")
    op.drop_index("ix_program_exam_requirements_program_id", table_name="program_exam_requirements")
    op.drop_table("program_exam_requirements")
    op.drop_index("ix_education_exams_code", table_name="education_exams")
    op.drop_table("education_exams")
    op.drop_index("ix_education_programs_code", table_name="education_programs")
    op.drop_index("ix_education_programs_institution_id", table_name="education_programs")
    op.drop_table("education_programs")
    op.drop_index("ix_education_institutions_code", table_name="education_institutions")
    op.drop_table("education_institutions")
