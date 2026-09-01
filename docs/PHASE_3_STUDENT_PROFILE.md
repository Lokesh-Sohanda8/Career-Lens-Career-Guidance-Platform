# CareerLens — Phase 3: Student Profile

## Goal

Create the canonical student context required by later assessments and recommendations.

```text
Authenticated User
       ↓
Student Profile
       ├── Academic Records
       ├── Interests
       ├── Preferences
       ├── Goals
       └── Constraints
```

## Implemented

- one-to-one user/student relationship
- profile creation
- profile retrieval
- profile update
- academic records
- interests
- preferences
- goals
- constraints
- ownership through authenticated user
- relational constraints and indexes
- Alembic migration

## API

```text
POST  /api/v1/students/me
GET   /api/v1/students/me
PATCH /api/v1/students/me

POST /api/v1/students/me/academic-records
POST /api/v1/students/me/interests
POST /api/v1/students/me/preferences
POST /api/v1/students/me/goals
POST /api/v1/students/me/constraints
```

## Intentionally not included

- assessments
- scoring
- careers
- recommendation logic
- AI
- skill inference
- education matching

## Exit Criteria

See `source_of_truth.md` → Phase 3 Definition of Done.
