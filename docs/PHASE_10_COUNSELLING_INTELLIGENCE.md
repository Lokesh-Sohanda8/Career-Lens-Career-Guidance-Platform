# CareerLens — Phase 10: Counselling Intelligence

## Goal

Create a structured guidance layer that helps students record concerns, decisions, goals, and follow-up actions using the intelligence already produced by CareerLens.

## Architecture

```text
Profile + Assessment + Recommendations
                +
Education + Learning
                ↓
       Counselling Context
                ↓
       Counselling Session
          /     |      \
       Notes Decisions Actions
                |
              Goals
                ↓
          Follow-up Work
```

## Implemented

- counselling sessions
- session status and topic
- student-owned counselling notes
- decisions with rationale/confidence
- action items with priority and lifecycle
- student counselling goals
- authenticated ownership
- API contracts
- Alembic migration
- unit coverage

## APIs

```text
GET   /api/v1/counselling/sessions
POST  /api/v1/counselling/sessions
PATCH /api/v1/counselling/sessions/{session_id}

POST  /api/v1/counselling/sessions/{session_id}/notes
POST  /api/v1/counselling/sessions/{session_id}/decisions
POST  /api/v1/counselling/sessions/{session_id}/actions

PATCH /api/v1/counselling/actions/{action_id}

GET   /api/v1/counselling/goals
POST  /api/v1/counselling/goals
PATCH /api/v1/counselling/goals/{goal_id}
```

## Important boundary

Phase 10 is the structured counselling domain.

It does NOT implement the AI counsellor.

It does not:

- diagnose mental-health conditions
- provide medical advice
- make high-stakes personal decisions for students
- fabricate counselling notes
- silently overwrite canonical career/education/skill data
- treat AI-generated guidance as authoritative

The later AI layer may read structured counselling context, but the domain remains the system of record for sessions, decisions, goals, and actions.

## Ownership

Counselling owns counselling records.

Career owns career truth.

Education owns education truth.

Learning owns learning progress.

Recommendation owns ranking.

Student Profile owns identity and student attributes.
