"""Create Career Intelligence tables.

Revision ID: 20260901_0004
Revises: 20260901_0003
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0004"
down_revision = "20260901_0003"
branch_labels = None
depends_on = None

uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "career_categories",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_career_categories_code", "career_categories", ["code"])

    op.create_table(
        "careers",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("category_id", uuid, sa.ForeignKey("career_categories.id", ondelete="SET NULL"), nullable=True),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("work_environment", sa.String(500), nullable=True),
        sa.Column("education_summary", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_careers_category_id", "careers", ["category_id"])
    op.create_index("ix_careers_code", "careers", ["code"])

    op.create_table(
        "career_requirements",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("career_id", uuid, sa.ForeignKey("careers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("requirement_type", sa.String(50), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("importance", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("career_id", "requirement_type", "name", name="uq_career_requirement"),
    )
    op.create_index("ix_career_requirements_career_id", "career_requirements", ["career_id"])

    op.create_table(
        "career_education_paths",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("career_id", uuid, sa.ForeignKey("careers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("program_name", sa.String(250), nullable=False),
        sa.Column("degree_level", sa.String(100), nullable=True),
        sa.Column("subject_area", sa.String(200), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("career_id", "program_name", name="uq_career_education_path"),
    )
    op.create_index("ix_career_education_paths_career_id", "career_education_paths", ["career_id"])


def downgrade() -> None:
    op.drop_index("ix_career_education_paths_career_id", table_name="career_education_paths")
    op.drop_table("career_education_paths")
    op.drop_index("ix_career_requirements_career_id", table_name="career_requirements")
    op.drop_table("career_requirements")
    op.drop_index("ix_careers_code", table_name="careers")
    op.drop_index("ix_careers_category_id", table_name="careers")
    op.drop_table("careers")
    op.drop_index("ix_career_categories_code", table_name="career_categories")
    op.drop_table("career_categories")
