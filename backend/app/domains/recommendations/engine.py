"""Deterministic CareerLens recommendation engine v1.

The engine is deliberately transparent. It combines explicit student interests,
assessment evidence, and career skill gaps. It is not an AI model and does not
claim to predict a student's future.
"""


class RecommendationEngineV1:
    VERSION = "v1"

    FACTORS = {
        "assessment_fit": 0.45,
        "interest_fit": 0.25,
        "skill_fit": 0.30,
    }

    @classmethod
    def recommend(cls, careers, student, skill_evidence, assessment_result=None, limit=5):
        assessment_traits = (
            assessment_result.result_payload.get("normalized_traits", {})
            if assessment_result else {}
        )
        interest_map = {
            item.interest.strip().lower(): (item.level or 1) / 5.0
            for item in student.interests
        }
        skill_map = {
            item.skill_id: (item.level or 0) / 5.0
            for item in skill_evidence
        }

        results = []
        for career in careers:
            assessment_fit = cls._assessment_fit(career, assessment_traits)
            interest_fit = cls._interest_fit(career, interest_map)
            skill_fit, gaps = cls._skill_fit(career, skill_map)

            score = (
                assessment_fit * cls.FACTORS["assessment_fit"]
                + interest_fit * cls.FACTORS["interest_fit"]
                + skill_fit * cls.FACTORS["skill_fit"]
            )
            evidence = []
            if assessment_fit > 0:
                evidence.append({"factor": "assessment_fit", "detail": f"Assessment alignment: {assessment_fit:.2f}"})
            if interest_fit > 0:
                evidence.append({"factor": "interest_fit", "detail": f"Interest alignment: {interest_fit:.2f}"})
            if skill_fit > 0:
                evidence.append({"factor": "skill_fit", "detail": f"Current skill coverage: {skill_fit:.2f}"})
            if gaps:
                evidence.append({"factor": "skill_gaps", "detail": f"{len(gaps)} skill gap(s) identified"})

            confidence = cls._confidence(assessment_result, interest_fit, skill_fit)
            explanation = cls._explain(career.title, assessment_fit, interest_fit, skill_fit, gaps)

            results.append({
                "career_id": career.id,
                "score": round(score, 4),
                "confidence": round(confidence, 4),
                "evidence": evidence,
                "gaps": gaps,
                "explanation": explanation,
            })

        results.sort(key=lambda x: (x["score"], x["confidence"]), reverse=True)
        for index, item in enumerate(results[:limit], start=1):
            item["rank"] = index
        return results[:limit]

    @staticmethod
    def _assessment_fit(career, traits):
        values = [float(traits[r.name]) for r in career.requirements if r.name in traits]
        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def _interest_fit(career, interests):
        matches = [value for r in career.requirements if r.requirement_type == "interest"
                   for key, value in interests.items() if key == r.name.strip().lower()]
        return sum(matches) / len(matches) if matches else 0.0

    @staticmethod
    def _skill_fit(career, skill_map):
        skill_reqs = list(getattr(career, "skill_requirements", []))
        if not skill_reqs:
            return 0.0, []
        covered = 0.0
        gaps = []
        for req in skill_reqs:
            current = skill_map.get(req.skill_id, 0.0)
            required = max(1, min(5, req.required_level)) / 5.0
            covered += min(current / required, 1.0) if required else 0.0
            if current < required:
                gaps.append(req.name)
        return covered / len(skill_reqs), gaps

    @staticmethod
    def _confidence(assessment_result, interest_fit, skill_fit):
        signals = int(assessment_result is not None) + int(interest_fit > 0) + int(skill_fit > 0)
        return signals / 3.0

    @staticmethod
    def _explain(title, assessment_fit, interest_fit, skill_fit, gaps):
        parts = [f"{title} received a preliminary fit score from available evidence."]
        if assessment_fit:
            parts.append(f"Assessment alignment is {assessment_fit:.2f}.")
        if interest_fit:
            parts.append(f"Interest alignment is {interest_fit:.2f}.")
        if skill_fit:
            parts.append(f"Current skill coverage is {skill_fit:.2f}.")
        if gaps:
            parts.append("Priority gaps: " + ", ".join(gaps[:5]) + ".")
        return " ".join(parts)
