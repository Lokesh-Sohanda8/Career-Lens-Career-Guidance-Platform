"""Create student profile tables.

Revision ID: 20260901_0002
Revises: 20260901_0001
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0002"
down_revision = "20260901_0001"
branch_labels = None
depends_on = None

uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", uuid, primary_key=True, nullable=False),
        sa.Column("user_id", uuid, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("current_grade", sa.String(50), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_students_user_id", "students", ["user_id"])

    op.create_table(
        "academic_records",
        sa.Column("id", uuid, primary_key=True, nullable=False),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject", sa.String(100), nullable=False),
        sa.Column("academic_year", sa.String(20), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("grade", sa.String(10), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("student_id", "subject", "academic_year", name="uq_academic_record_student_subject_year"),
    )
    op.create_index("ix_academic_records_student_id", "academic_records", ["student_id"])

    for table, columns, constraint in [
        ("student_interests", [("interest", sa.String(150), False), ("level", sa.Integer(), True)], "uq_student_interest"),
        ("student_preferences", [("key", sa.String(100), False), ("value", sa.String(500), False)], "uq_student_preference"),
    ]:
        op.create_table(
            table,
            sa.Column("id", uuid, primary_key=True, nullable=False),
            sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
            *[sa.Column(n, t, nullable=not nullable) for n, t, nullable in columns],
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("student_id", columns[0][0], name=constraint),
        )
        op.create_index(f"ix_{table}_student_id", table, ["student_id"])

    op.create_table(
        "student_goals",
        sa.Column("id", uuid, primary_key=True, nullable=False),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_student_goals_student_id", "student_goals", ["student_id"])

    op.create_table(
        "student_constraints",
        sa.Column("id", uuid, primary_key=True, nullable=False),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("key", sa.String(100), nullable=False),
        sa.Column("value", sa.String(500), nullable=False),
        sa.Column("importance", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_student_constraints_student_id", "student_constraints", ["student_id"])


def downgrade() -> None:
    op.drop_index("ix_student_constraints_student_id", table_name="student_constraints")
    op.drop_table("student_constraints")
    op.drop_index("ix_student_goals_student_id", table_name="student_goals")
    op.drop_table("student_goals")
    op.drop_index("ix_student_preferences_student_id", table_name="student_preferences")
    op.drop_table("student_preferences")
    op.drop_index("ix_student_interests_student_id", table_name="student_interests")
    op.drop_table("student_interests")
    op.drop_index("ix_academic_records_student_id", table_name="academic_records")
    op.drop_table("academic_records")
    op.drop_index("ix_students_user_id", table_name="students")
    op.drop_table("students")
