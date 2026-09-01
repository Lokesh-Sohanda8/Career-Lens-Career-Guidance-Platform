"""Build a bounded, deterministic AI context from canonical domains."""

import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.recommendations.models import RecommendationRun
from app.domains.student.models import Student
from app.domains.skills.models import StudentSkillEvidence
from app.domains.counselling.models import CounsellingGoal


class AIContextBuilder:
    VERSION = "v1"

    def __init__(self, session: AsyncSession):
        self.session = session

    async def build_for_student(self, student_id):
        result = await self.session.execute(
            select(Student)
            .where(Student.id == student_id)
            .options(
                selectinload(Student.academic_records),
                selectinload(Student.interests),
                selectinload(Student.preferences),
                selectinload(Student.goals),
                selectinload(Student.constraints),
            )
        )
        student = result.scalar_one_or_none()
        if not student:
            return None

        rec_result = await self.session.execute(
            select(RecommendationRun)
            .where(RecommendationRun.student_id == student_id)
            .options(selectinload(RecommendationRun.items))
            .order_by(RecommendationRun.created_at.desc())
            .limit(1)
        )
        recommendation = rec_result.scalar_one_or_none()

        goal_result = await self.session.execute(
            select(CounsellingGoal)
            .where(CounsellingGoal.student_id == student_id)
            .order_by(CounsellingGoal.priority.desc())
            .limit(10)
        )
        counselling_goals = list(goal_result.scalars().all())

        evidence_result = await self.session.execute(
            select(StudentSkillEvidence).where(StudentSkillEvidence.student_id == student_id)
        )
        skill_evidence = list(evidence_result.scalars().all())

        payload = {
            "student": {
                "first_name": student.first_name,
                "current_grade": student.current_grade,
                "bio": student.bio,
            },
            "academics": [
                {"subject": x.subject, "academic_year": x.academic_year,
                 "score": x.score, "grade": x.grade}
                for x in student.academic_records
            ],
            "interests": [
                {"interest": x.interest, "level": x.level}
                for x in student.interests
            ],
            "preferences": [{"key": x.key, "value": x.value} for x in student.preferences],
            "goals": [
                {"title": x.title, "description": x.description, "priority": x.priority}
                for x in student.goals
            ],
            "constraints": [
                {"key": x.key, "value": x.value, "importance": x.importance}
                for x in student.constraints
            ],
            "skill_evidence": [
                {"skill_id": str(x.skill_id), "evidence_type": x.evidence_type,
                 "score": x.score, "source": x.source}
                for x in skill_evidence
            ],
            "latest_recommendations": [
                {
                    "career_id": str(x.career_id),
                    "rank": x.rank,
                    "score": x.score,
                    "confidence": x.confidence,
                    "gaps": x.gaps,
                    "explanation": x.explanation,
                }
                for x in (recommendation.items if recommendation else [])
            ],
            "counselling_goals": [
                {"title": x.title, "status": x.status, "priority": x.priority}
                for x in counselling_goals
            ],
        }
        return payload

    @classmethod
    def to_prompt_context(cls, payload) -> str:
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)
