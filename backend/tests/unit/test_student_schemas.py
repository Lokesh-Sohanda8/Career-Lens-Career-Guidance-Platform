from datetime import date

import pytest
from pydantic import ValidationError

from app.domains.student.schemas import AcademicRecordCreate, GoalCreate, InterestCreate


def test_academic_score_is_bounded():
    with pytest.raises(ValidationError):
        AcademicRecordCreate(subject="Math", academic_year="2026", score=101)


def test_interest_level_is_bounded():
    with pytest.raises(ValidationError):
        InterestCreate(interest="Technology", level=6)


def test_goal_priority_is_bounded():
    with pytest.raises(ValidationError):
        GoalCreate(title="Learn Python", priority=0)


def test_valid_goal():
    goal = GoalCreate(title="Learn Python", priority=5, target_date=date(2027, 1, 1))
    assert goal.priority == 5
