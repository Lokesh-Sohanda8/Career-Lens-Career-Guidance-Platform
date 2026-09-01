"""Central SQLAlchemy model registry."""

from app.domains.identity.models import Role, User, user_roles  # noqa: F401
from app.domains.student.models import (
    AcademicRecord, Student, StudentConstraint, StudentGoal,
    StudentInterest, StudentPreference,
)
from app.domains.assessments.models import (
    Assessment, AssessmentVersion, AssessmentDimension, AssessmentQuestion,
    AssessmentOption, AssessmentSession, AssessmentResponse, AssessmentResult,
)
from app.domains.careers.models import (
    Career, CareerCategory, CareerRequirement, CareerEducationPath,
)
from app.domains.skills.models import (
    Skill, SkillCategory, CareerSkillRequirement, StudentSkillEvidence,
)
from app.domains.recommendations.models import (
    RecommendationRun, RecommendationItem, RecommendationFactor,
)
from app.domains.education.models import (
    EducationInstitution, EducationProgram, EducationExam,
    ProgramExamRequirement, ProgramEligibilityRule, CareerEducationProgram,
)
from app.domains.learning.models import (
    LearningResource, ResourceSkill, LearningPath, LearningPathStep,
    LearningPathResource, StudentLearningPlan, StudentLearningProgress,
)
from app.domains.counselling.models import (
    CounsellingSession, CounsellingNote, CounsellingDecision,
    CounsellingActionItem, CounsellingGoal,
)
from app.domains.reports.models import Report, ReportSection
from app.domains.ai.models import AIInteraction

__all__ = [
    "Role", "User", "user_roles", "Student", "AcademicRecord",
    "StudentInterest", "StudentPreference", "StudentGoal", "StudentConstraint",
    "Assessment", "AssessmentVersion", "AssessmentDimension", "AssessmentQuestion",
    "AssessmentOption", "AssessmentSession", "AssessmentResponse", "AssessmentResult",
    "Career", "CareerCategory", "CareerRequirement", "CareerEducationPath",
    "Skill", "SkillCategory", "CareerSkillRequirement", "StudentSkillEvidence",
    "RecommendationRun", "RecommendationItem", "RecommendationFactor",
    "EducationInstitution", "EducationProgram", "EducationExam",
    "ProgramExamRequirement", "ProgramEligibilityRule", "CareerEducationProgram",
    "LearningResource", "ResourceSkill", "LearningPath", "LearningPathStep",
    "LearningPathResource", "StudentLearningPlan", "StudentLearningProgress",
    "CounsellingSession", "CounsellingNote", "CounsellingDecision",
    "CounsellingActionItem", "CounsellingGoal",
    "Report", "ReportSection", "AIInteraction",
]
