from types import SimpleNamespace
from uuid import uuid4

from app.domains.recommendations.engine import RecommendationEngineV1


def test_recommendation_engine_ranks_matching_career():
    req = SimpleNamespace(name="analytical", requirement_type="trait", importance=5)
    career = SimpleNamespace(id=uuid4(), title="Data Scientist", requirements=[req])
    student = SimpleNamespace(interests=[])

    assessment = SimpleNamespace(
        result_payload={"normalized_traits": {"analytical": 1.0}}
    )

    result = RecommendationEngineV1.recommend(
        [career], student, [], assessment_result=assessment, limit=5
    )

    assert result[0]["career_id"] == career.id
    assert result[0]["rank"] == 1
    assert result[0]["score"] > 0
    assert result[0]["confidence"] > 0
