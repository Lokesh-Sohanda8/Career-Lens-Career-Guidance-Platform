"""Create Reports tables.

Revision ID: 20260901_0010
Revises: 20260901_0009
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0010"
down_revision = "20260901_0009"
branch_labels = None
depends_on = None
uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("report_type", sa.String(60), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("status", sa.String(40), nullable=False, server_default="generated"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_snapshot", sa.Text(), nullable=False),
    )
    op.create_index("ix_reports_student_id", "reports", ["student_id"])

    op.create_table(
        "report_sections",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("report_id", uuid, sa.ForeignKey("reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_key", sa.String(100), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("section_order", sa.Integer(), nullable=False),
        sa.UniqueConstraint("report_id", "section_order", name="uq_report_section_order"),
    )
    op.create_index("ix_report_sections_report_id", "report_sections", ["report_id"])


def downgrade() -> None:
    op.drop_index("ix_report_sections_report_id", table_name="report_sections")
    op.drop_table("report_sections")
    op.drop_index("ix_reports_student_id", table_name="reports")
    op.drop_table("reports")
