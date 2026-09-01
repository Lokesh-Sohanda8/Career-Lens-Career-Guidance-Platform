# CareerLens — Phase 5: Career Intelligence

## Goal

Build the canonical career knowledge layer used by future recommendation logic.

## Flow

```text
Career Catalog
     ↓
Career Categories
     ↓
Career Requirements
     ↓
Career ↔ Education Paths
     ↓
Student Evidence
     ↓
Preliminary Candidate Generation
```

## Implemented

- career categories
- careers
- career requirements
- career education paths
- active career catalog API
- career detail API
- transparent preliminary candidate generation
- optional use of a completed assessment result
- migration
- unit test

## API

```text
GET  /api/v1/careers
GET  /api/v1/careers/{career_id}
POST /api/v1/careers/candidates
```

## Important boundary

This phase creates the **career intelligence/catalog layer** and a preliminary candidate generator.

It does NOT implement the final recommendation engine.

The final recommendation engine remains Phase 7 and will own:

- recommendation runs
- formal scoring
- factor weights
- confidence
- evidence aggregation
- recommendation snapshots
- history

## Data principle

Career records are canonical product data. They should eventually be populated from curated, versioned sources. The application does not invent career truth through an LLM.

## Intentionally not included

- skill catalog
- final career ranking
- recommendation snapshots
- AI explanations
- RAG
- education institution matching
- admission prediction
