from app.domains.counselling.models import (
    CounsellingActionItem, CounsellingDecision, CounsellingGoal,
    CounsellingNote, CounsellingSession,
)


def test_counselling_domain_models_are_available():
    assert CounsellingSession.__tablename__ == "counselling_sessions"
    assert CounsellingNote.__tablename__ == "counselling_notes"
    assert CounsellingDecision.__tablename__ == "counselling_decisions"
    assert CounsellingActionItem.__tablename__ == "counselling_action_items"
    assert CounsellingGoal.__tablename__ == "counselling_goals"
