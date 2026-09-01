from types import SimpleNamespace
from uuid import uuid4

from app.domains.careers.candidate_generation import CareerCandidateGenerator


def test_candidate_generation_uses_explicit_interest():
    category = SimpleNamespace(name="Technology")
    requirement = SimpleNamespace(name="Python", importance=5)
    career = SimpleNamespace(
        id=uuid4(),
        title="Data Scientist",
        category=category,
        requirements=[requirement],
    )
    student = SimpleNamespace(
        interests=[SimpleNamespace(interest="Python", level=5)],
        academic_records=[],
    )

    result = CareerCandidateGenerator.generate([career], student)

    assert len(result) == 1
    assert result[0]["title"] == "Data Scientist"
    assert result[0]["preliminary_score"] > 0
