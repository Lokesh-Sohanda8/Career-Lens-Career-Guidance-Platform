"""Deterministic skill-gap analysis."""
class SkillGapAnalyzer:
    @staticmethod
    def analyze(requirements, evidence):
        emap={e.skill_id:e for e in evidence}; gaps=[]
        for req in requirements:
            item=emap.get(req.skill_id); current=item.level if item else 0; gap=max(req.required_level-current,0)
            gaps.append({"skill_id":req.skill_id,"skill_name":req.skill.name,"required_level":req.required_level,"current_level":current,"gap":gap,"importance":req.importance,"priority_score":round((gap/5)*(req.importance/5),4),"evidence_source":item.source_type if item else None})
        return sorted(gaps,key=lambda x:(x["priority_score"],x["gap"]),reverse=True)
