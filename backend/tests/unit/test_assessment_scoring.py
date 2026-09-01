from types import SimpleNamespace
from uuid import uuid4

from app.domains.assessments.scoring import AssessmentScoringEngine


def test_scoring_normalizes_five_point_scale():
    dimension_id = uuid4()
    question_id = uuid4()
    option_id = uuid4()

    dimension = SimpleNamespace(id=dimension_id, code="analytical")
    option = SimpleNamespace(id=option_id, score=5)
    question = SimpleNamespace(id=question_id, dimension_id=dimension_id, options=[option])

    version = SimpleNamespace(
        dimensions=[dimension],
        questions=[question],
    )
    response = SimpleNamespace(question_id=question_id, selected_option_id=option_id)

    result = AssessmentScoringEngine.score(version, [response])

    assert result["scores"]["analytical"] == 5
    assert result["normalized_traits"]["analytical"] == 1.0
