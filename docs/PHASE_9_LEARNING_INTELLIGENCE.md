# CareerLens — Phase 9: Learning Intelligence

## Goal

Turn identified skill gaps and career pathways into structured learning paths and trackable student plans.

## Architecture

```text
Career Recommendation
       +
Skill Gaps
       +
Learning Knowledge
       ↓
Learning Path
       ↓
Ordered Steps
       ↓
Resources
       ↓
Student Learning Plan
       ↓
Progress Tracking
```

## Implemented

- learning resource catalog
- resource ↔ skill mapping
- reusable learning paths
- ordered learning path steps
- path ↔ career targeting
- step ↔ resource mapping
- student-owned learning plans
- per-step progress
- plan-level progress aggregation
- deterministic path prioritization foundation
- authenticated ownership
- migration
- unit test

## APIs

```text
GET   /api/v1/learning/resources
GET   /api/v1/learning/paths
GET   /api/v1/learning/paths/{path_id}

POST  /api/v1/learning/plans
PATCH /api/v1/learning/plans/{plan_id}/progress
```

## Important boundary

This phase manages structured learning knowledge and progress.

It does NOT:

- generate courses with an LLM
- claim that completing a resource guarantees a skill level
- scrape arbitrary content
- recommend unsafe or unverified resources
- replace formal education requirements
- predict career outcomes

Learning content should be curated and versioned.

## Progress model

Each plan contains step-level progress from 0–100%.

Plan progress is the average of its step progress values.

A plan becomes `completed` when all step progress reaches 100%.
