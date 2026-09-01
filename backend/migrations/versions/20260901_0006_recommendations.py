"""Create recommendation engine tables.

Revision ID: 20260901_0006
Revises: 20260901_0005
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0006"
down_revision = "20260901_0005"
branch_labels = None
depends_on = None
uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "recommendation_runs",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assessment_session_id", uuid, sa.ForeignKey("assessment_sessions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("engine_version", sa.String(50), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_recommendation_runs_student_id", "recommendation_runs", ["student_id"])
    op.create_index("ix_recommendation_runs_assessment_session_id", "recommendation_runs", ["assessment_session_id"])

    op.create_table(
        "recommendation_factors",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("run_id", uuid, sa.ForeignKey("recommendation_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("factor_code", sa.String(100), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("run_id", "factor_code", name="uq_recommendation_factor"),
    )
    op.create_index("ix_recommendation_factors_run_id", "recommendation_factors", ["run_id"])

    op.create_table(
        "recommendation_items",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("run_id", uuid, sa.ForeignKey("recommendation_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("career_id", uuid, sa.ForeignKey("careers.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("gaps", sa.JSON(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.UniqueConstraint("run_id", "rank", name="uq_recommendation_item_rank"),
    )
    op.create_index("ix_recommendation_items_run_id", "recommendation_items", ["run_id"])
    op.create_index("ix_recommendation_items_career_id", "recommendation_items", ["career_id"])


def downgrade() -> None:
    op.drop_index("ix_recommendation_items_career_id", table_name="recommendation_items")
    op.drop_index("ix_recommendation_items_run_id", table_name="recommendation_items")
    op.drop_table("recommendation_items")
    op.drop_index("ix_recommendation_factors_run_id", table_name="recommendation_factors")
    op.drop_table("recommendation_factors")
    op.drop_index("ix_recommendation_runs_assessment_session_id", table_name="recommendation_runs")
    op.drop_index("ix_recommendation_runs_student_id", table_name="recommendation_runs")
    op.drop_table("recommendation_runs")
