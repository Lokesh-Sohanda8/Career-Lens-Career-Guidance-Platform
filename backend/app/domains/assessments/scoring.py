"""Deterministic assessment scoring."""

from collections import defaultdict


class AssessmentScoringEngine:
    VERSION = "v1"

    @classmethod
    def score(cls, version, responses):
        dimensions = {d.id: d for d in version.dimensions}
        question_map = {q.id: q for q in version.questions}
        option_map = {o.id: o for q in version.questions for o in q.options}

        totals = defaultdict(float)
        counts = defaultdict(int)

        for response in responses:
            question = question_map.get(response.question_id)
            option = option_map.get(response.selected_option_id)
            if not question or not option:
                continue
            dimension = dimensions.get(question.dimension_id)
            if not dimension:
                continue
            totals[dimension.code] += option.score
            counts[dimension.code] += 1

        raw_scores = dict(totals)
        normalized = {}
        for code, total in raw_scores.items():
            count = counts[code]
            # Scores are expected to use a 1–5 option scale by convention for v1.
            normalized[code] = round(max(0.0, min(1.0, ((total / count) - 1) / 4)), 4) if count else 0.0

        return {
            "scores": {k: round(v, 4) for k, v in raw_scores.items()},
            "normalized_traits": normalized,
        }
