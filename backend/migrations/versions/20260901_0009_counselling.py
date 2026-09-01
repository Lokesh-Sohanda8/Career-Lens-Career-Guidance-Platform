"""Create Counselling Intelligence tables.

Revision ID: 20260901_0009
Revises: 20260901_0008
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0009"
down_revision = "20260901_0008"
branch_labels = None
depends_on = None
uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "counselling_sessions",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_type", sa.String(60), nullable=False, server_default="career_guidance"),
        sa.Column("status", sa.String(40), nullable=False, server_default="open"),
        sa.Column("primary_topic", sa.String(250), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_counselling_sessions_student_id", "counselling_sessions", ["student_id"])

    op.create_table(
        "counselling_notes",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("session_id", uuid, sa.ForeignKey("counselling_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("note_type", sa.String(50), nullable=False, server_default="observation"),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source", sa.String(40), nullable=False, server_default="student"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_counselling_notes_session_id", "counselling_notes", ["session_id"])

    op.create_table(
        "counselling_decisions",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("session_id", uuid, sa.ForeignKey("counselling_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("decision_type", sa.String(60), nullable=False),
        sa.Column("decision", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("confidence", sa.String(30), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_counselling_decisions_session_id", "counselling_decisions", ["session_id"])

    op.create_table(
        "counselling_action_items",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("session_id", uuid, sa.ForeignKey("counselling_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("action_type", sa.String(60), nullable=False, server_default="general"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("status", sa.String(40), nullable=False, server_default="open"),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_counselling_action_items_session_id", "counselling_action_items", ["session_id"])

    op.create_table(
        "counselling_goals",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(250), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(40), nullable=False, server_default="active"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("target_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("student_id", "title", name="uq_counselling_student_goal"),
    )
    op.create_index("ix_counselling_goals_student_id", "counselling_goals", ["student_id"])


def downgrade() -> None:
    op.drop_index("ix_counselling_goals_student_id", table_name="counselling_goals")
    op.drop_table("counselling_goals")
    op.drop_index("ix_counselling_action_items_session_id", table_name="counselling_action_items")
    op.drop_table("counselling_action_items")
    op.drop_index("ix_counselling_decisions_session_id", table_name="counselling_decisions")
    op.drop_table("counselling_decisions")
    op.drop_index("ix_counselling_notes_session_id", table_name="counselling_notes")
    op.drop_table("counselling_notes")
    op.drop_index("ix_counselling_sessions_student_id", table_name="counselling_sessions")
    op.drop_table("counselling_sessions")
