# CareerLens — Phase 6: Skill Intelligence

## Goal
Create a canonical skill layer connecting careers to required skills and students to evidence of current skill levels.

## Flow
```text
Skill Catalog
    ↓
Career ↔ Skill Requirements
    ↓
Student Skill Evidence
    ↓
Skill Gap Analysis
    ↓
Priority Gaps
```

## Implemented
- skill categories
- skill catalog
- career-skill requirements
- student skill evidence
- evidence source + confidence
- deterministic skill-gap analysis
- gap priority score
- authenticated student ownership
- migration
- unit tests

## API
```text
GET /api/v1/skills
GET /api/v1/skills/{skill_id}
GET /api/v1/skills/me/evidence
PUT /api/v1/skills/me/evidence
GET /api/v1/skills/me/gaps/{career_id}
```

## Skill scale
`0–5` is the application skill-level scale. `0` means no recorded evidence; `5` is the highest configured level.

## Evidence principle
A student skill level is evidence, not an objective truth. `source_type`, `confidence`, and `evidence_note` are retained so future recommendation logic can distinguish stronger from weaker evidence.

## Gap logic
`gap = max(required_level - current_level, 0)`.

`priority_score = (gap / 5) × (importance / 5)`.

This is a transparent MVP prioritization rule, not a labor-market prediction or psychometric measure.

## Boundary
Phase 6 owns the skill catalog, career-skill requirements, student skill evidence, and gap analysis.
Phase 7 owns final recommendation scoring, ranking, confidence, evidence aggregation, and recommendation snapshots.
