"""Deterministic career candidate generation.

This phase intentionally provides a transparent, preliminary candidate generator.
It does not produce the final CareerLens recommendation or claim predictive validity.
"""

from collections import Counter


class CareerCandidateGenerator:
    """Generate preliminary career candidates from explicit student evidence."""

    @staticmethod
    def generate(careers, student, assessment_result=None):
        signals = Counter()

        # Explicit student interests are strong candidate-generation signals.
        for item in student.interests:
            signals[item.interest.strip().lower()] += item.level or 1

        # Academic subjects are additional signals.
        for record in student.academic_records:
            signals[record.subject.strip().lower()] += 1

        candidates = []
        for career in careers:
            evidence = []
            score = 0.0

            for req in career.requirements:
                req_name = req.name.strip().lower()
                if req_name in signals:
                    contribution = min(1.0, signals[req_name] / 5.0) * (req.importance / 5.0)
                    score += contribution
                    evidence.append(f"Matched explicit student signal: {req.name}")

            # Assessment results are evidence only when a dimension code directly
            # matches a career requirement name. This keeps the mapping explicit.
            if assessment_result:
                normalized = assessment_result.result_payload.get("normalized_traits", {})
                for req in career.requirements:
                    value = normalized.get(req.name)
                    if value is not None:
                        score += float(value) * (req.importance / 5.0)
                        evidence.append(f"Assessment evidence: {req.name}")

            if score > 0:
                candidates.append({
                    "career_id": career.id,
                    "title": career.title,
                    "category": career.category.name if career.category else None,
                    "evidence": evidence,
                    "preliminary_score": round(min(score, 1.0), 4),
                })

        return sorted(candidates, key=lambda item: item["preliminary_score"], reverse=True)
