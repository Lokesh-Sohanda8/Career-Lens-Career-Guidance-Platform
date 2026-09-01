from types import SimpleNamespace
from uuid import uuid4

from app.domains.learning.planner import LearningPlannerV1


def test_learning_planner_prefers_path_with_matching_gap():
    matching = SimpleNamespace(
        title="Python Foundations",
        steps=[SimpleNamespace(title="Python", skill_id=None)],
    )
    other = SimpleNamespace(
        title="Communication Basics",
        steps=[SimpleNamespace(title="Presentation", skill_id=None)],
    )

    ranked = LearningPlannerV1.prioritize_paths([other, matching], ["Python"])

    assert ranked[0].title == "Python Foundations"
