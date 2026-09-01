"""Deterministic learning-plan selection."""

class LearningPlannerV1:
    VERSION = "v1"

    @staticmethod
    def prioritize_paths(paths, gaps):
        gap_names = {name.strip().lower() for name in gaps}
        ranked = []
        for path in paths:
            matching = 0
            for step in path.steps:
                if step.title.strip().lower() in gap_names:
                    matching += 1
                if step.skill_id and str(step.skill_id).lower() in gap_names:
                    matching += 1
            ranked.append((matching, path))
        ranked.sort(key=lambda item: (item[0], item[1].title), reverse=True)
        return [path for _, path in ranked]
