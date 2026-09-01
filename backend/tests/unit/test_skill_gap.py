from types import SimpleNamespace
from uuid import uuid4
from app.domains.skills.gap_analysis import SkillGapAnalyzer

def test_gap_priority_orders_high_importance_gap():
    sid=uuid4()
    req=SimpleNamespace(skill_id=sid,skill=SimpleNamespace(name="Python"),required_level=5,importance=5)
    evidence=SimpleNamespace(skill_id=sid,level=2,source_type="self_report")
    result=SkillGapAnalyzer.analyze([req],[evidence])
    assert result[0]["gap"]==3
    assert result[0]["priority_score"]==0.6

def test_missing_evidence_is_zero_current_level():
    sid=uuid4()
    req=SimpleNamespace(skill_id=sid,skill=SimpleNamespace(name="SQL"),required_level=4,importance=3)
    result=SkillGapAnalyzer.analyze([req],[])
    assert result[0]["current_level"]==0
    assert result[0]["gap"]==4
