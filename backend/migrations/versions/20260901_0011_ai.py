"""Create AI interaction audit table.

Revision ID: 20260901_0011
Revises: 20260901_0010
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0011"
down_revision = "20260901_0010"
branch_labels = None
depends_on = None
uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "ai_interactions",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("task_type", sa.String(60), nullable=False),
        sa.Column("provider", sa.String(80), nullable=False),
        sa.Column("model", sa.String(150), nullable=False),
        sa.Column("prompt_version", sa.String(40), nullable=False),
        sa.Column("context_version", sa.String(40), nullable=False),
        sa.Column("input_hash", sa.String(64), nullable=False),
        sa.Column("response_text", sa.Text(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="completed"),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("error_code", sa.String(80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ai_interactions_student_id", "ai_interactions", ["student_id"])


def downgrade() -> None:
    op.drop_index("ix_ai_interactions_student_id", table_name="ai_interactions")
    op.drop_table("ai_interactions")
