"""Create Learning Intelligence tables.

Revision ID: 20260901_0008
Revises: 20260901_0007
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260901_0008"
down_revision = "20260901_0007"
branch_labels = None
depends_on = None
uuid = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "learning_resources",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("code", sa.String(150), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("resource_type", sa.String(80), nullable=False),
        sa.Column("provider_name", sa.String(200), nullable=True),
        sa.Column("url", sa.String(1000), nullable=True),
        sa.Column("difficulty", sa.String(50), nullable=True),
        sa.Column("estimated_minutes", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_learning_resources_code", "learning_resources", ["code"])

    op.create_table(
        "resource_skills",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("resource_id", uuid, sa.ForeignKey("learning_resources.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill_id", uuid, sa.ForeignKey("skills.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("relevance", sa.Integer(), nullable=False, server_default="3"),
        sa.UniqueConstraint("resource_id", "skill_id", name="uq_resource_skill"),
    )
    op.create_index("ix_resource_skills_resource_id", "resource_skills", ["resource_id"])
    op.create_index("ix_resource_skills_skill_id", "resource_skills", ["skill_id"])

    op.create_table(
        "learning_paths",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("code", sa.String(150), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("target_career_id", uuid, sa.ForeignKey("careers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_learning_paths_code", "learning_paths", ["code"])
    op.create_index("ix_learning_paths_target_career_id", "learning_paths", ["target_career_id"])

    op.create_table(
        "learning_path_steps",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("path_id", uuid, sa.ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill_id", uuid, sa.ForeignKey("skills.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), nullable=True),
        sa.UniqueConstraint("path_id", "step_order", name="uq_learning_path_step_order"),
    )
    op.create_index("ix_learning_path_steps_path_id", "learning_path_steps", ["path_id"])
    op.create_index("ix_learning_path_steps_skill_id", "learning_path_steps", ["skill_id"])

    op.create_table(
        "learning_path_resources",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("step_id", uuid, sa.ForeignKey("learning_path_steps.id", ondelete="CASCADE"), nullable=False),
        sa.Column("resource_id", uuid, sa.ForeignKey("learning_resources.id", ondelete="RESTRICT"), nullable=False),
        sa.UniqueConstraint("step_id", "resource_id", name="uq_learning_path_resource"),
    )
    op.create_index("ix_learning_path_resources_step_id", "learning_path_resources", ["step_id"])
    op.create_index("ix_learning_path_resources_resource_id", "learning_path_resources", ["resource_id"])

    op.create_table(
        "student_learning_plans",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("student_id", uuid, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("path_id", uuid, sa.ForeignKey("learning_paths.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("status", sa.String(40), nullable=False, server_default="active"),
        sa.Column("progress_percent", sa.Float(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("student_id", "path_id", name="uq_student_learning_plan"),
    )
    op.create_index("ix_student_learning_plans_student_id", "student_learning_plans", ["student_id"])
    op.create_index("ix_student_learning_plans_path_id", "student_learning_plans", ["path_id"])

    op.create_table(
        "student_learning_progress",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("plan_id", uuid, sa.ForeignKey("student_learning_plans.id", ondelete="CASCADE"), nullable=False),
        sa.Column("step_id", uuid, sa.ForeignKey("learning_path_steps.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(40), nullable=False, server_default="not_started"),
        sa.Column("progress_percent", sa.Float(), nullable=False, server_default="0"),
        sa.Column("last_completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("plan_id", "step_id", name="uq_student_learning_progress"),
    )
    op.create_index("ix_student_learning_progress_plan_id", "student_learning_progress", ["plan_id"])
    op.create_index("ix_student_learning_progress_step_id", "student_learning_progress", ["step_id"])


def downgrade() -> None:
    op.drop_index("ix_student_learning_progress_step_id", table_name="student_learning_progress")
    op.drop_index("ix_student_learning_progress_plan_id", table_name="student_learning_progress")
    op.drop_table("student_learning_progress")
    op.drop_index("ix_student_learning_plans_path_id", table_name="student_learning_plans")
    op.drop_index("ix_student_learning_plans_student_id", table_name="student_learning_plans")
    op.drop_table("student_learning_plans")
    op.drop_index("ix_learning_path_resources_resource_id", table_name="learning_path_resources")
    op.drop_index("ix_learning_path_resources_step_id", table_name="learning_path_resources")
    op.drop_table("learning_path_resources")
    op.drop_index("ix_learning_path_steps_skill_id", table_name="learning_path_steps")
    op.drop_index("ix_learning_path_steps_path_id", table_name="learning_path_steps")
    op.drop_table("learning_path_steps")
    op.drop_index("ix_learning_paths_target_career_id", table_name="learning_paths")
    op.drop_index("ix_learning_paths_code", table_name="learning_paths")
    op.drop_table("learning_paths")
    op.drop_index("ix_resource_skills_skill_id", table_name="resource_skills")
    op.drop_index("ix_resource_skills_resource_id", table_name="resource_skills")
    op.drop_table("resource_skills")
    op.drop_index("ix_learning_resources_code", table_name="learning_resources")
    op.drop_table("learning_resources")
