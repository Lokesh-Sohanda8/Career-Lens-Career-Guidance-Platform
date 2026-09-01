# CareerLens — Phase 8: Education Intelligence

## Goal

Connect career recommendations to structured education pathways without pretending to predict admissions.

## Architecture

```text
Career
  ↓
Career ↔ Education Program
  ↓
Institution
  +
Program
  +
Eligibility Rules
  +
Exam Requirements
  ↓
Student Academic Evidence
  ↓
Education Matcher v1
  ↓
Pathway Match + Verification Status
```

## Implemented

- institution catalog
- program catalog
- exam catalog
- program exam requirements
- structured eligibility rules
- career-to-program relationships
- program detail API
- deterministic education matching
- authenticated student ownership
- unit tests
- Alembic migration

## APIs

```text
GET /api/v1/education/institutions
GET /api/v1/education/exams
GET /api/v1/education/programs
GET /api/v1/education/programs/{program_id}
GET /api/v1/education/matches/{career_id}
```

## Matching rules

The first matcher supports:

- `subject_min_score`
- `overall_percentage`

Unknown rule types are returned as `needs_verification`.

## Important boundary

This module evaluates structured pathway fit from known data.

It does NOT:

- predict admission probability
- guarantee eligibility
- infer missing academic facts
- rank colleges by prestige
- use an LLM as an eligibility authority
- replace official institution/exam requirements

Official eligibility should always be verified against the current institution or examination authority.

## Data principle

Education records are canonical product data. They should be curated, versioned, and refreshed as official requirements change.
