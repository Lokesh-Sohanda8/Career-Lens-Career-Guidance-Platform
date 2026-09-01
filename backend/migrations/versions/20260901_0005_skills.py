"""Create Skill Intelligence tables.
Revision ID: 20260901_0005
Revises: 20260901_0004
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="20260901_0005"
down_revision="20260901_0004"
branch_labels=None
depends_on=None
uuid=postgresql.UUID(as_uuid=True)
def upgrade():
    op.create_table("skill_categories",sa.Column("id",uuid,primary_key=True),sa.Column("code",sa.String(100),nullable=False),sa.Column("name",sa.String(200),nullable=False),sa.Column("description",sa.Text(),nullable=True),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("code"))
    op.create_index("ix_skill_categories_code","skill_categories",["code"])
    op.create_table("skills",sa.Column("id",uuid,primary_key=True),sa.Column("category_id",uuid,sa.ForeignKey("skill_categories.id",ondelete="SET NULL"),nullable=True),sa.Column("code",sa.String(100),nullable=False),sa.Column("name",sa.String(200),nullable=False),sa.Column("description",sa.Text(),nullable=True),sa.Column("is_active",sa.Boolean(),nullable=False,server_default=sa.true()),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("code"))
    op.create_index("ix_skills_category_id","skills",["category_id"]); op.create_index("ix_skills_code","skills",["code"])
    op.create_table("career_skill_requirements",sa.Column("id",uuid,primary_key=True),sa.Column("career_id",uuid,sa.ForeignKey("careers.id",ondelete="CASCADE"),nullable=False),sa.Column("skill_id",uuid,sa.ForeignKey("skills.id",ondelete="CASCADE"),nullable=False),sa.Column("required_level",sa.Integer(),nullable=False),sa.Column("importance",sa.Integer(),nullable=False,server_default="3"),sa.Column("notes",sa.Text(),nullable=True),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("career_id","skill_id",name="uq_career_skill_requirement"))
    op.create_index("ix_career_skill_requirements_career_id","career_skill_requirements",["career_id"]); op.create_index("ix_career_skill_requirements_skill_id","career_skill_requirements",["skill_id"])
    op.create_table("student_skill_evidence",sa.Column("id",uuid,primary_key=True),sa.Column("student_id",uuid,sa.ForeignKey("students.id",ondelete="CASCADE"),nullable=False),sa.Column("skill_id",uuid,sa.ForeignKey("skills.id",ondelete="RESTRICT"),nullable=False),sa.Column("level",sa.Integer(),nullable=False),sa.Column("confidence",sa.Integer(),nullable=False,server_default="3"),sa.Column("source_type",sa.String(50),nullable=False),sa.Column("evidence_note",sa.Text(),nullable=True),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.Column("updated_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("student_id","skill_id",name="uq_student_skill_evidence"))
    op.create_index("ix_student_skill_evidence_student_id","student_skill_evidence",["student_id"]); op.create_index("ix_student_skill_evidence_skill_id","student_skill_evidence",["skill_id"])
def downgrade():
    op.drop_index("ix_student_skill_evidence_skill_id",table_name="student_skill_evidence"); op.drop_index("ix_student_skill_evidence_student_id",table_name="student_skill_evidence"); op.drop_table("student_skill_evidence")
    op.drop_index("ix_career_skill_requirements_skill_id",table_name="career_skill_requirements"); op.drop_index("ix_career_skill_requirements_career_id",table_name="career_skill_requirements"); op.drop_table("career_skill_requirements")
    op.drop_index("ix_skills_code",table_name="skills"); op.drop_index("ix_skills_category_id",table_name="skills"); op.drop_table("skills")
    op.drop_index("ix_skill_categories_code",table_name="skill_categories"); op.drop_table("skill_categories")
