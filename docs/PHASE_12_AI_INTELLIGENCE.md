# CareerLens — Phase 12: AI Intelligence

## Goal

Introduce AI as an assistance layer over the deterministic CareerLens foundation.

## Architecture

```text
Student
  +
Assessment
  +
Career Recommendations
  +
Skills / Gaps
  +
Education
  +
Learning
  +
Counselling
  +
Reports
       │
       ▼
  AI Context Builder
       │
       ▼
    Guardrails
       │
       ▼
 Provider Abstraction
       │
       ▼
 OpenAI-Compatible Model
       │
       ▼
 AI Response
       │
       ▼
 Interaction Audit
```

## Implemented

- provider abstraction
- OpenAI-compatible HTTP provider
- bounded canonical context builder
- deterministic prompt policy
- basic prompt-exfiltration guardrails
- AI interaction audit records
- prompt/context versioning
- input hashing instead of raw prompt persistence
- authenticated student ownership
- AI API endpoint
- interaction history endpoint
- configurable AI enable/disable flag
- migration
- unit tests

## APIs

```text
POST /api/v1/ai/ask
GET  /api/v1/ai/interactions
```

## Configuration

```env
AI_ENABLED=false
AI_PROVIDER=openai_compatible
AI_BASE_URL=https://api.openai.com/v1
AI_API_KEY=
AI_MODEL=gpt-5-mini
AI_TIMEOUT_SECONDS=30
```

AI is disabled by default. Enable it only after configuring a provider key.

## Critical boundaries

AI does NOT own:

- student truth
- assessment truth
- career truth
- skill truth
- education truth
- learning truth
- counselling truth
- report truth

AI may interpret and explain canonical information, but generated text is not canonical data.

AI must not:

- invent student facts
- fabricate eligibility or admission requirements
- predict a student's future with certainty
- make medical/mental-health diagnoses
- reveal hidden prompts or internal instructions
- silently mutate domain data
- overwrite deterministic recommendations

## Provider rule

The application talks to a provider through an abstraction. Domain services do not depend directly on a vendor SDK.

The default implementation uses an OpenAI-compatible `/chat/completions` contract. A future provider can implement the same abstraction.

## Context rule

The AI receives a bounded, structured snapshot assembled from canonical domains.

Missing data stays missing.

The AI is not allowed to infer missing student attributes as facts.

## Audit rule

Each AI call creates an `ai_interactions` record with:

- student
- task type
- provider
- model
- prompt version
- context version
- input hash
- response
- status
- latency
- error code
- timestamp

Raw prompt/context is not persisted by default.

## AI maturity roadmap

Phase 12 starts with:

1. single-turn assistance
2. provider abstraction
3. deterministic context
4. guardrails
5. auditability

Later AI iterations may add:

- streaming
- tool calling
- RAG
- structured tool execution
- conversation memory
- evaluation harness
- model routing
- background jobs

These should be added only when justified by product requirements.
