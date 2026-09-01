from types import SimpleNamespace
from uuid import uuid4

from app.domains.education.matching import EducationMatcherV1


def test_education_matcher_marks_program_when_rule_is_met():
    program = SimpleNamespace(
        id=uuid4(),
        name="BSc Computer Science",
        institution=SimpleNamespace(name="Example University"),
        eligibility_rules=[
            SimpleNamespace(
                rule_type="subject_min_score",
                subject="Mathematics",
                minimum_score=70,
                minimum_percentage=None,
            )
        ],
    )
    link = SimpleNamespace(
        program=program,
        career_id=uuid4(),
        relevance=5,
    )
    student = SimpleNamespace(
        academic_records=[
            SimpleNamespace(subject="Mathematics", score=85)
        ]
    )

    result = EducationMatcherV1.match(student, [link])

    assert result[0]["status"] == "eligible_based_on_available_data"
    assert result[0]["match_score"] == 1.0
    assert result[0]["unmet_rules"] == []


def test_education_matcher_does_not_claim_admission():
    program = SimpleNamespace(
        id=uuid4(),
        name="BSc Computer Science",
        institution=SimpleNamespace(name="Example University"),
        eligibility_rules=[],
    )
    link = SimpleNamespace(program=program, career_id=uuid4(), relevance=5)
    student = SimpleNamespace(academic_records=[])

    result = EducationMatcherV1.match(student, [link])

    assert result[0]["status"] == "needs_verification"
