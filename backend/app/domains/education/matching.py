"""Deterministic education/program matching.

This module assesses pathway fit from available student academic evidence and
structured eligibility rules. It does not predict admission.
"""

class EducationMatcherV1:
    VERSION = "v1"

    @staticmethod
    def match(student, career_links):
        records = {
            record.subject.strip().lower(): record
            for record in student.academic_records
        }

        results = []
        for link in career_links:
            program = link.program
            reasons = []
            unmet = []
            checks = []

            for rule in program.eligibility_rules:
                if rule.rule_type == "subject_min_score" and rule.subject:
                    record = records.get(rule.subject.strip().lower())
                    if record is None or record.score is None:
                        unmet.append(f"Missing score for {rule.subject}.")
                        continue
                    checks.append(1 if record.score >= (rule.minimum_score or 0) else 0)
                    if record.score >= (rule.minimum_score or 0):
                        reasons.append(f"{rule.subject} meets the minimum score.")
                    else:
                        unmet.append(
                            f"{rule.subject} score is below {rule.minimum_score}."
                        )
                elif rule.rule_type == "overall_percentage":
                    scores = [r.score for r in student.academic_records if r.score is not None]
                    if not scores:
                        unmet.append("Overall academic percentage is unavailable.")
                        continue
                    percentage = sum(scores) / len(scores)
                    checks.append(1 if percentage >= (rule.minimum_percentage or 0) else 0)
                    if percentage >= (rule.minimum_percentage or 0):
                        reasons.append("Available academic scores meet the overall threshold.")
                    else:
                        unmet.append(
                            f"Available academic average is below {rule.minimum_percentage}%."
                        )
                else:
                    unmet.append(f"Rule requires verification: {rule.rule_type}.")

            score = sum(checks) / len(checks) if checks else 0.0
            if not program.eligibility_rules:
                status = "needs_verification"
                reasons.append("No structured eligibility rules are recorded.")
            elif unmet:
                status = "needs_verification"
            else:
                status = "eligible_based_on_available_data"

            results.append({
                "program_id": program.id,
                "program_name": program.name,
                "institution_name": program.institution.name,
                "career_id": link.career_id,
                "relevance": link.relevance,
                "match_score": round(score * (link.relevance / 5.0), 4),
                "status": status,
                "reasons": reasons,
                "unmet_rules": unmet,
            })

        return sorted(
            results,
            key=lambda x: (x["match_score"], x["relevance"]),
            reverse=True,
        )
