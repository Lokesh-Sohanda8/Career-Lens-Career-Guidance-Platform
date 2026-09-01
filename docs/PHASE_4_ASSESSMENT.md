# CareerLens — Phase 4: Assessment

## Goal

Create a versioned assessment system that can define assessments, questions, dimensions, sessions, responses, deterministic scoring, and persisted results.

## Flow

```text
Assessment
   ↓
Published Version
   ↓
Dimensions + Questions + Options
   ↓
Student Session
   ↓
Responses
   ↓
Deterministic Scoring
   ↓
Assessment Result
```

## Implemented

- assessment catalog
- assessment versions
- dimensions
- questions
- options
- assessment sessions
- responses
- deterministic scoring v1
- normalized traits
- persisted results
- authenticated student ownership
- migration
- unit scoring test

## API

```text
GET  /api/v1/assessments
GET  /api/v1/assessments/{assessment_id}
POST /api/v1/assessments/{assessment_id}/sessions
POST /api/v1/assessments/sessions/{session_id}/responses
POST /api/v1/assessments/sessions/{session_id}/complete
```

## Important design decision

The scoring engine is deterministic. No LLM is involved.

Assessment version and scoring version are persisted so a result remains explainable after future scoring changes.

## Current scoring convention

Version `v1` expects option scores on a 1–5 scale and normalizes the average dimension score to 0–1.

This is an implementation convention, not the final psychometric methodology. The product must not claim psychometric validity until an appropriate validated assessment methodology is selected and documented.

## Intentionally not included

- career recommendation
- AI interpretation
- RAG
- psychometric claims beyond the actual configured assessment
- career scoring
- skill inference
