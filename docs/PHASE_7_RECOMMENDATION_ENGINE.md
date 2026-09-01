# CareerLens — Phase 7: Recommendation Engine

## Goal

Turn the evidence layers built in Phases 3–6 into a deterministic, versioned, explainable recommendation run.

## Evidence flow

```text
Student Profile
     +
Assessment Result
     +
Student Interests
     +
Skill Evidence
     +
Career Knowledge
     ↓
Recommendation Engine v1
     ↓
Ranked Careers
     ↓
Evidence + Gaps + Confidence
     ↓
Recommendation Run Snapshot
```

## Implemented

- recommendation runs
- engine versioning
- explicit factor weights
- recommendation items
- evidence
- skill gaps
- confidence
- explanations
- recommendation history
- immutable run records after creation
- authenticated student ownership
- deterministic ranking
- unit test

## v1 factors

```text
assessment_fit = 0.45
interest_fit   = 0.25
skill_fit      = 0.30
```

Final score:

```text
score =
    assessment_fit × 0.45
  + interest_fit   × 0.25
  + skill_fit      × 0.30
```

## Important boundary

The engine is deterministic. No LLM is used.

AI interpretation and richer explanations remain later work.

## Important limitation

The weights and scoring rules are product-engineering defaults. They are not statistically validated and must not be represented as scientifically predictive.

## API

```text
POST /api/v1/recommendations/generate
GET  /api/v1/recommendations/{run_id}
GET  /api/v1/recommendations/history
```
