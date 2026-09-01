"""Create assessment domain tables.

Revision ID: 20260901_0003
Revises: 20260901_0002
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0003"
down_revision = "20260901_0002"
branch_labels = None
depends_on = None

uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "assessments",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_assessments_code", "assessments", ["code"])

    op.create_table(
        "assessment_versions",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("assessment_id", uuid, sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=True),
        sa.Column("scoring_version", sa.String(50), nullable=False, server_default="v1"),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("assessment_id", "version", name="uq_assessment_version"),
    )
    op.create_index("ix_assessment_versions_assessment_id", "assessment_versions", ["assessment_id"])

    op.create_table(
        "assessment_dimensions",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("assessment_version_id", uuid, sa.ForeignKey("assessment_versions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("assessment_version_id", "code", name="uq_assessment_dimension_code"),
    )
    op.create_index("ix_assessment_dimensions_assessment_version_id", "assessment_dimensions", ["assessment_version_id"])

    op.create_table(
        "assessment_questions",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("assessment_version_id", uuid, sa.ForeignKey("assessment_versions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("dimension_id", uuid, sa.ForeignKey("assessment_dimensions.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("question_number", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("question_type", sa.String(50), nullable=False, server_default="single_choice"),
        sa.Column("is_required", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("assessment_version_id", "question_number", name="uq_assessment_question_number"),
    )
    op.create_index("ix_assessment_questions_assessment_version_id", "assessment_questions", ["assessment_version_id"])
    op.create_index("ix_assessment_questions_dimension_id", "assessment_questions", ["dimension_id"])

    op.create_table(
        "assessment_options",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("question_id", uuid, sa.ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("option_number", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(500), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("question_id", "option_number", name="uq_assessment_option_number"),
    )
    op.create_index("ix_assessment_options_question_id", "assessment_options", ["question_id"])

    op.create_table(
        "assessment_sessions",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assessment_version_id", uuid, sa.ForeignKey("assessment_versions.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="in_progress"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_assessment_sessions_student_id", "assessment_sessions", ["student_id"])
    op.create_index("ix_assessment_sessions_assessment_version_id", "assessment_sessions", ["assessment_version_id"])

    op.create_table(
        "assessment_responses",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("session_id", uuid, sa.ForeignKey("assessment_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_id", uuid, sa.ForeignKey("assessment_questions.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("selected_option_id", uuid, sa.ForeignKey("assessment_options.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("session_id", "question_id", name="uq_assessment_response_question"),
    )
    op.create_index("ix_assessment_responses_session_id", "assessment_responses", ["session_id"])
    op.create_index("ix_assessment_responses_question_id", "assessment_responses", ["question_id"])

    op.create_table(
        "assessment_results",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("session_id", uuid, sa.ForeignKey("assessment_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scoring_version", sa.String(50), nullable=False),
        sa.Column("result_payload", sa.JSON(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("session_id"),
    )
    op.create_index("ix_assessment_results_session_id", "assessment_results", ["session_id"])


def downgrade() -> None:
    op.drop_index("ix_assessment_results_session_id", table_name="assessment_results")
    op.drop_table("assessment_results")
    op.drop_index("ix_assessment_responses_question_id", table_name="assessment_responses")
    op.drop_index("ix_assessment_responses_session_id", table_name="assessment_responses")
    op.drop_table("assessment_responses")
    op.drop_index("ix_assessment_sessions_assessment_version_id", table_name="assessment_sessions")
    op.drop_index("ix_assessment_sessions_student_id", table_name="assessment_sessions")
    op.drop_table("assessment_sessions")
    op.drop_index("ix_assessment_options_question_id", table_name="assessment_options")
    op.drop_table("assessment_options")
    op.drop_index("ix_assessment_questions_dimension_id", table_name="assessment_questions")
    op.drop_index("ix_assessment_questions_assessment_version_id", table_name="assessment_questions")
    op.drop_table("assessment_questions")
    op.drop_index("ix_assessment_dimensions_assessment_version_id", table_name="assessment_dimensions")
    op.drop_table("assessment_dimensions")
    op.drop_index("ix_assessment_versions_assessment_id", table_name="assessment_versions")
    op.drop_table("assessment_versions")
    op.drop_index("ix_assessments_code", table_name="assessments")
    op.drop_table("assessments")
