## 2026-09-01 — AI as an assistance layer

Decision:

Introduce AI only after the deterministic product domains are established.

Reason:

AI should interpret and assist with existing CareerLens intelligence rather than becoming the system of record.

---

## 2026-09-01 — Provider abstraction

Decision:

Do not couple CareerLens domain services directly to a specific model vendor.

Reason:

Provider/model choice will change. A stable application-level contract allows providers to be changed without rewriting domain logic.

---

## 2026-09-01 — AI interaction audit

Decision:

Persist AI interaction metadata and response for auditability while storing an input hash instead of the raw prompt/context by default.

Reason:

AI behavior needs observability and traceability while minimizing unnecessary persistence of sensitive user context.

---

## 2026-09-01 — Reports as snapshots

Decision:

Reports are immutable-style snapshots of structured CareerLens state rather than canonical data stores.

Reason:

Historical reports must remain auditable even when student profiles, recommendations, education rules, learning progress, or counselling records change later.

---

## 2026-09-01 — Presentation deferred

Decision:

Keep report storage separate from PDF/document rendering.

Reason:

The reporting domain should establish stable structured output first. Rendering formats can consume the same snapshot without coupling core business logic to a presentation format.

---

## 2026-09-01 — Counselling Intelligence domain

Decision:

Create a dedicated Counselling domain for sessions, notes, decisions, action items, and student goals.

Reason:

Guidance needs a durable, auditable workflow layer before conversational AI is introduced. This allows later AI capabilities to operate over structured context rather than becoming the system of record.

---

## 2026-09-01 — AI counsellor deferred

Decision:

Do not implement an AI counsellor in Phase 10.

Reason:

The deterministic product domains must establish the student's canonical context first. AI should consume that context and assist with guidance later rather than becoming the source of truth.

---

# CareerLens — SOURCE OF TRUTH / THE BIBLE

> **Status:** Authoritative  
> **Version:** 12.1.0  
> **Last Updated:** 2026-09-01  
> **Current Phase:** Phase 12 — AI Intelligence  
> **Purpose:** This document is the permanent architectural, product, engineering, and decision source of truth for CareerLens.

---

## 0. How to Use This File

This file is the **Bible of CareerLens**.

Before making a significant architectural, database, API, product, security, or AI decision:

1. Read this file.
2. Identify the relevant rule or decision.
3. Check whether the proposed change conflicts with it.
4. If it does conflict, do not silently change the architecture.
5. Either preserve the current decision or explicitly update this file with the reason, impact, and migration plan.

### Recovery rule

If the codebase becomes confusing, incomplete, corrupted, or partially rebuilt:

> **Reconstruct the system from this file, not from the existing code.**

Code is implementation.  
This document is the authoritative intent.

---

# 1. Product Identity

## Product

**CareerLens**

## Category

AI + Human Career Intelligence and Career Counselling Platform.

## Product Definition

CareerLens is an evidence-driven career intelligence platform that combines assessments, personal context, career and education intelligence, AI assistance, and human counselling to help people make better-informed career decisions and act on them.

## Core philosophy

CareerLens is a **decision-support system**, not a deterministic life-prediction system.

The system should help answer:

- Why might this career fit me?
- What evidence supports that?
- What are the alternatives?
- What gaps exist?
- What constraints matter?
- What education pathways are relevant?
- What should I do next?
- When is human counselling valuable?

---

# 2. Non-Negotiable Product Principles

1. Recommendations must not be presented as absolute truths.
2. Evidence must be distinguishable by source and strength.
3. Structured data is the canonical source of truth.
4. Deterministic intelligence must produce core recommendation results.
5. AI is an assistance layer, not the foundation.
6. Human counsellors can review, challenge, confirm, reject, or override automated recommendations.
7. Important recommendation inputs and outputs must be versioned.
8. Recommendations must be explainable and auditable.
9. User privacy and control are first-class requirements.
10. Build the product vertically, not as a collection of disconnected modules.

---

# 3. Current Product Journey

```text
Registration
  ↓
Student Profile
  ↓
Academic Information
  ↓
Interests & Preferences
  ↓
Psychometric Assessment
  ↓
Assessment Interpretation
  ↓
Career Candidate Generation
  ↓
Career Compatibility
  ↓
Career Ranking
  ↓
Evidence & Explanation
  ↓
Skill Gap Analysis
  ↓
Education / Course Pathway
  ↓
College / Program Matching
  ↓
Action Plan
  ↓
Human Counsellor Review
  ↓
Final Guidance Report
```

---

# 4. MVP Boundary

## MVP includes

- Identity and access
- Student profile
- Academic information
- Interests, preferences, goals, constraints
- Assessment system
- Career catalog and requirements
- Career-skill relationships
- Career-education relationships
- Compatibility and ranking
- Skill gaps
- Education/program matching
- Learning paths
- Counselling workflow
- Reports

## Explicitly not MVP

- Multi-agent AI
- Autonomous agents
- Advanced RAG
- Microservices
- Complex orchestration
- Real-time collaboration
- Marketplace
- Payments/subscriptions
- Institute SaaS
- Mobile app
- Large-scale data pipelines
- Admission probability prediction
- Palmistry automation
- Neuroscience inference
- Massive external integrations

---

# 5. Architecture Decision Record — Current State

## ADR-001: Modular Monolith

**Decision:** CareerLens starts as a modular monolith.

### Stack

```text
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Pydantic
```

### Reason

The product requires strong domain boundaries but does not yet require independently deployable services.

### Rule

Do not introduce microservices unless a concrete operational or scaling requirement justifies extraction.

---

# 6. High-Level Architecture

```text
Frontend
   ↓
REST API
   ↓
FastAPI API Layer
   ↓
Domain Services
   ↓
Repositories
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

AI, when introduced:

```text
Canonical Data
   ↓
Deterministic Intelligence
   ↓
Evidence Aggregation
   ↓
Recommendation Engine
   ↓
AI Explanation / Assistance
```

Never:

```text
User
 ↓
LLM
 ↓
Business Truth
```

---

# 7. Backend Domain Map

Current intended domains:

```text
identity
student
assessments
careers
skills
education
learning
recommendations
counselling
reports
```

### Ownership

| Domain | Owns |
|---|---|
| Identity | users, authentication, roles, account state |
| Student | profile, academics, interests, preferences, goals, constraints |
| Assessments | definitions, questions, sessions, responses, scoring, results |
| Careers | career catalog, categories, requirements |
| Skills | skill catalog, career requirements, student skill evidence, gaps |
| Education | institutions, programs, exams, eligibility |
| Learning | resources, paths, milestones, progress |
| Recommendations | recommendation runs, scoring, evidence aggregation, snapshots |
| Counselling | counsellors, cases, sessions, observations, human decisions |
| Reports | report generation, snapshots, sections, exports |

### Ownership rule

A domain owns its **canonical data**.

The Recommendation domain may consume Career and Skill data, but should not duplicate ownership of those records.

---

# 8. Domain Internal Structure

Default structure:

```text
domain/
├── __init__.py
├── models.py
├── schemas.py
├── repository.py
└── service.py
```

Only add files such as:

```text
scoring.py
compatibility.py
events.py
candidate_generation.py
```

when a real domain requirement exists.

Do not create abstraction layers merely for architectural appearance.

---

# 9. API Convention

Base path:

```text
/api/v1
```

Current API groups:

```text
/api/v1/auth
/api/v1/users
/api/v1/students
/api/v1/assessments
/api/v1/careers
/api/v1/skills
/api/v1/education
/api/v1/learning
/api/v1/recommendations
/api/v1/counselling
/api/v1/reports
```

Do not create API modules for every tiny database concept.

---

# 10. Database Rules

PostgreSQL is the system of record.

Use:

- UUID identifiers
- foreign keys
- unique constraints
- indexes
- timestamps
- active/soft-delete state where appropriate
- audit fields where required
- Alembic migrations

Use JSON only for:

- flexible metadata
- versioned configuration
- extensible assessment metadata
- external provider payloads
- experimental data

Do not use JSON to avoid proper relational modeling.

---

# 11. Identity Domain — Phase 2

## Status

**COMPLETE — reconciled in v12.1.0.**

Identity is the account/access boundary. It owns `users`, `roles`, `user_roles`, authentication, and account state.

Student Profile is a separate domain. Identity does not own the `students` table and registration does not implicitly create a profile. The Student domain owns `students` and links each profile to its account through `students.user_id → users.id`.

### User

Canonical account entity:

```text
id
email
password_hash
is_active
created_at
updated_at
```

### Role

Canonical authorization role:

```text
id
name
created_at
```

Public registration assigns only the server-controlled `student` role. Privileged roles are never accepted from the client.

### Authentication

```text
OAuth2-compatible bearer token
JWT
```

The JWT stores the user UUID in `sub` and uses a configured expiration. Passwords are stored as bcrypt hashes only.

### Migration root

Identity migration `20260901_0001_identity` is mandatory because Student Profile migration `0002` and every later migration depend on it. A rebuild must preserve this root migration or intentionally replace the entire migration history.

# 12. Current Identity API

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/users/me
```

### Registration

Input:

```json
{
  "email": "student@example.com",
  "password": "secure-password"
}
```

Output excludes the password and password hash.

### Login

OAuth2 form:

```text
username = email
password = password
```

Returns:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### Current-user endpoint

```text
GET /api/v1/users/me
Authorization: Bearer <token>
```

Returns the authenticated user's identity and roles.

---

# 13. Security Rules

1. Never store plaintext passwords.
2. Never log passwords.
3. Never return password hashes through APIs.
4. Keep JWT secret outside source control.
5. Use environment configuration for secrets.
6. Validate authentication before protected operations.
7. Authorization must be explicit for privileged operations.
8. Do not trust role information supplied by the client.
9. Use HTTPS in deployed environments.
10. Keep authentication implementation behind the Identity domain so it can evolve without changing every feature.

---

# 14. Recommendation Architecture

The recommendation system is deterministic first.

```text
Student Evidence
      ↓
Evidence Aggregation
      ↓
Feature Normalization
      ↓
Candidate Generation
      ↓
Compatibility
      ↓
Ranking
      ↓
Explanation
      ↓
Recommendation Snapshot
```

Every recommendation run should eventually record:

- engine version
- input snapshot/version
- factors used
- factor weights
- candidate careers
- scores
- evidence
- confidence
- timestamp

The exact scoring formula is intentionally not fixed yet.

Do not scatter arbitrary weights through application code.

---

# 15. Evidence Model

Future canonical abstraction:

```text
Evidence
├── source_type
├── source_id
├── evidence_type
├── value
├── confidence
├── captured_at
├── method
├── engine_version
└── metadata
```

Potential sources:

- assessment
- academic record
- profile
- skill evidence
- counsellor
- education data
- user preference

---

# 16. Versioning Rules

Version anything that can change the explanation of a recommendation.

Minimum planned versions:

```text
Assessment Version
Scoring Version
Career Data Version
Recommendation Engine Version
Education Data Version
College Predictor Version
Report Version
```

Goal:

> Be able to explain what CareerLens knew and why it made a recommendation at a particular point in time.

---

# 17. AI Architecture

AI is now an assistance layer over the deterministic product. Phase 12 implements the first provider-agnostic AI slice. Future capabilities include:

- conversational career guidance
- explanations
- report drafting
- counsellor assistance
- question generation
- resource summaries
- personalized learning explanations
- research assistance
- RAG

AI must consume structured/canonical information.

AI must not silently modify canonical career, assessment, eligibility, or recommendation truth.

---

# 18. Counselling Architecture

Human counselling is a core product capability.

```text
Structured Intelligence
       ↓
Preliminary Analysis
       ↓
Human Counsellor
       ↓
Review / Challenge / Context
       ↓
Final Guidance
```

Human decisions must be stored separately from automated scores.

---

# 19. Production Engineering Rules

From the beginning:

- environment-based configuration
- secrets outside source code
- structured logging
- request IDs
- consistent errors
- validation
- migrations
- authentication
- authorization
- health checks
- readiness checks
- automated tests
- CI
- linting
- formatting
- static checks
- dependency pinning
- security checks
- API versioning

Do not add infrastructure solely to make the repository look sophisticated.

---

# 20. Testing Rules

### Unit tests

Test:

- validation
- scoring
- business rules
- ranking
- eligibility
- security primitives

### Integration tests

Test:

- database operations
- authentication
- APIs
- domain interactions

### E2E

Maintain at least one complete product journey.

---

# 21. Vertical Slice Strategy

Do not build:

```text
80 tables
→
100 endpoints
→
AI
→
connect everything
```

Build:

```text
Feature
 ↓
Model
 ↓
Repository
 ↓
Service
 ↓
API
 ↓
Frontend
 ↓
Test
```

---

# 22. Phase Plan

## Phase 1 — Foundation

Status: **COMPLETE**

Includes:

- repository structure
- configuration
- FastAPI
- PostgreSQL connection
- SQLAlchemy
- Alembic
- base setup
- error handling
- logging
- health/readiness
- testing foundation

## Phase 2 — Identity

Status: **IN PROGRESS / CURRENT**

Includes:

- users
- authentication
- roles
- student identity

## Phase 3 — Student Profile

Includes:

- student profile
- academic records
- interests
- preferences
- goals
- constraints

## Phase 4 — Assessment

Includes:

- definitions
- versions
- dimensions
- questions
- options
- sessions
- responses
- scoring
- results

## Phase 5 — Career Intelligence

Status: **COMPLETE**

Includes:

- career catalog
- categories
- career requirements
- career-education mapping
- preliminary candidate generation

Career-skill mapping is implemented in Phase 6 because the Skill domain owns the canonical skill relationship. Final compatibility, ranking, confidence, and recommendation snapshots belong to Phase 7.

## Phase 6 — Skill Intelligence

Status: **COMPLETE**

Includes:

- skill categories
- skill catalog
- career-skill requirements
- student skill evidence
- evidence source and confidence
- deterministic skill-gap analysis
- gap priorities

## Phase 7 — Recommendation Engine

Status: **COMPLETE**

Includes:

- recommendation runs
- evidence aggregation
- score calculation
- confidence
- snapshots
- history

## Phase 8 — Education

Status: **COMPLETE**

Includes:

- institutions
- programs
- relationships
- exams
- eligibility
- preferences
- matching

## Phase 9 — Learning

Status: **COMPLETE**

Includes:

- resources
- resource-skill relationships
- paths
- milestones
- progress

## Phase 10 — Counselling

Status: **COMPLETE**

Includes:

- counsellors
- cases
- sessions
- observations
- recommendation review
- human override
- final guidance

## Phase 11 — Reports

Status: **COMPLETE**

Includes:

- recommendation report
- evidence report
- career action plan
- counsellor report

## Phase 12 — AI

Status: **CURRENT**

Includes:

- AI career assistant
- AI explanations
- report drafting
- counsellor copilot
- RAG
- guardrails
- evaluation
- observability

---

# 23. Current Build Order

```text
Phase 1  Foundation       ✅
Phase 2  Identity         ✅ RECONCILED
Phase 3  Student          ✅
Phase 4  Assessment       ✅
Phase 5  Careers          ✅
Phase 6  Skills           ✅
Phase 7  Recommendations  ✅
Phase 8  Education        ✅
Phase 9  Learning         ✅
Phase 10 Counselling      ✅
Phase 11 Reports          ✅
Phase 12 AI               🚧 CURRENT
```

Phase 2 is no longer an exception. Its implementation and documentation now agree.

---

# 24. Definition of Done — Identity

Phase 2 is complete because:

- a user can register
- duplicate email registration is rejected
- passwords are bcrypt-hashed
- public registration assigns the server-controlled `student` role
- a user can log in
- a JWT is issued with configured expiration
- authenticated `/users/me` works
- invalid credentials are rejected
- inactive users cannot authenticate
- protected routes reject missing/invalid tokens
- identity roles are loaded without requiring lazy-loading after the DB session closes
- database migration `0001_identity` recreates the identity tables
- downstream migration `0002_student_profile` can safely reference identity
- security-critical unit tests cover the configuration/role/password contract
- Identity remains separate from Student Profile ownership

# 25. Current Repository Reality

The source code is an implementation of this document.

When code and this document disagree:

1. determine whether the disagreement is intentional;
2. if intentional, update this document;
3. if unintentional, correct the code;
4. never silently let architecture drift.

---

# 26. Decision Log

## 2026-09-01 — Skill Intelligence domain

Decision:

Create a dedicated Skill Intelligence domain for the canonical skill catalog, career-skill requirements, student skill evidence, and skill-gap analysis.

Reason:

Skills are shared knowledge entities used by careers, recommendations, education, and future learning paths. They require a stable domain boundary before recommendation scoring is introduced.

---

## 2026-09-01 — Evidence-aware skill gaps

Decision:

Store student skill level, evidence source, confidence, and note separately from career required levels.

Reason:

CareerLens must distinguish between a claimed skill and stronger evidence. This also makes future evidence aggregation possible without changing the core schema.

---

## 2026-09-01 — Learning Intelligence domain

Decision:

Create a dedicated Learning domain for reusable learning resources, learning paths, ordered steps, resource mappings, student learning plans, and progress.

Reason:

Skill gaps are only useful if the product can translate them into actionable learning work while keeping learning content separate from career and education truth.

---

## 2026-09-01 — Deterministic learning progress

Decision:

Represent progress at the learning-step level and calculate plan progress as the average of step progress.

Reason:

A simple deterministic progress model is auditable and avoids inventing mastery from completion alone.

---

## 2026-09-01 — Education Intelligence domain

Decision:

Create a dedicated Education domain for institutions, programs, exams, eligibility rules, and career-to-program relationships.

Reason:

Education is a separate canonical knowledge layer that must remain independent from Career and Recommendation ownership.

---

## 2026-09-01 — Deterministic education pathway matching

Decision:

Use a deterministic matcher to compare available student academic evidence with structured program eligibility rules.

Reason:

Eligibility must be auditable and conservative. Missing or unsupported rules should produce verification requirements rather than invented conclusions.

---

## 2026-09-01 — Alembic revision chain reconciliation

Decision:

Correct the duplicate recommendation migration revision inherited from Phase 7 by moving recommendations to revision 0006 and reserving 0007 for Education.

Reason:

Alembic migrations must form a single valid lineage before production deployment.

---

## 2026-09-01 — Recommendation Engine domain

Decision:

Create a dedicated Recommendation domain responsible for recommendation runs, factor weights, ranking, evidence aggregation, confidence, and immutable result snapshots.

Reason:

Recommendation logic must remain separate from canonical Student, Assessment, Career, and Skill data.

---

## 2026-09-01 — Deterministic recommendation engine v1

Decision:

Use a deterministic weighted scoring engine for the first recommendation implementation. Store the engine version and factor weights with every run.

Reason:

The recommendation system must be reproducible, testable, explainable, and auditable before introducing AI.

---

## 2026-09-01 — Career Intelligence domain

Decision:

Create a canonical Career Intelligence domain for career categories, careers, career requirements, and career education paths.

Reason:

The recommendation engine needs a stable career knowledge layer before formal scoring and ranking can be implemented.

---

## 2026-09-01 — Preliminary candidate generation

Decision:

Introduce a transparent deterministic candidate generator in Phase 5, while reserving final recommendation scoring and snapshots for Phase 7.

Reason:

Candidate generation and recommendation ranking are separate responsibilities. Keeping them separate prevents premature coupling and makes the eventual recommendation engine easier to test and version.

---

## 2026-09-01 — Assessment domain

Decision:

Create a versioned Assessment domain containing assessment definitions, dimensions, questions, options, sessions, responses, scoring, and results.

Reason:

Assessment results are a core evidence source for CareerLens recommendations and must be reproducible and auditable.

---

## 2026-09-01 — Deterministic assessment scoring

Decision:

Assessment scoring is deterministic and versioned. No LLM is used in the scoring path.

Reason:

Core evidence must remain reproducible and independently auditable.

---

## 2026-09-01 — Clean rebuild

Decision:

Rebuild CareerLens from scratch rather than carrying forward the previous implementation architecture.

Reason:

The previous implementation introduced unnecessary architectural complexity.

---

## 2026-09-01 — Modular monolith

Decision:

Use FastAPI + PostgreSQL + SQLAlchemy + Alembic + Pydantic.

Reason:

Strong internal domain boundaries are sufficient at the current product stage.

---

## 2026-09-01 — Deterministic core before AI

Decision:

Do not build AI agents, RAG, or LLM orchestration before the deterministic career-decision workflow works.

Reason:

Career recommendations must be evidence-backed, reproducible, explainable, and auditable.

---

## 2026-09-01 — Identity implementation

Decision:

Implement users, roles, JWT authentication, and authenticated current-user access as the first real domain.

Reason:

All later student-facing workflows require a stable identity boundary.

---

# 27. Change Protocol

Whenever changing architecture, record:

```text
Date:
Decision:
Problem:
Current behavior:
Proposed behavior:
Reason:
Affected domains:
Affected database tables:
Affected APIs:
Migration required:
Backward compatibility:
Tests required:
Status:
```

Do not remove historical decisions. Mark them superseded instead.

---

# 28. Rebuild Protocol

If rebuilding CareerLens from scratch:

### Step 1

Read this document completely.

### Step 2

Restore the architecture:

```text
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Pydantic
```

### Step 3

Restore domains in phase order.

### Step 4

Restore only the current phase.

### Step 5

Run migrations.

### Step 6

Run tests.

### Step 7

Validate the current vertical slice.

### Step 8

Only then continue to the next phase.

---

# 29. Anti-Drift Rules

Do not introduce:

```text
microservices
agents
orchestrators
RAG
vector databases
Redis
Kafka
Celery
event buses
AI gateways
model routers
```

unless a documented decision demonstrates why the current architecture can no longer support the requirement.

Do not create empty placeholder domains.

Do not create duplicate models.

Do not create duplicate API modules.

Do not create generic "utils" for domain business logic.

Do not move business logic into API routes.

Do not make the LLM the source of truth.

---

# 30. The Three Questions Rule

Every new feature must answer:

### 1. What problem does this solve?

### 2. Which domain owns it?

### 3. What data is the source of truth?

If these cannot be answered clearly:

> **Do not implement the feature yet.**

---

# 31. Current Status

```text
PRODUCT IDEA              ✅
PRODUCT PHILOSOPHY        ✅
MVP                       ✅
ARCHITECTURE              ✅
DOMAIN BOUNDARIES         ✅
PHASE 1 FOUNDATION        ✅
PHASE 2 IDENTITY          ✅
PHASE 3 STUDENT PROFILE   ✅
PHASE 4 ASSESSMENT        ✅
PHASE 5 CAREER INTELLIGENCE ✅
PHASE 6 SKILL INTELLIGENCE  ✅
FIRST VERTICAL SLICE      ⏳
PRODUCTION DEPLOYMENT     ⏳
AI LAYER                  ⏳
```

---

# 32. Next Authorized Work

The current implementation target remains:

> **Continue Phase 12 — AI Intelligence.**

Phase 2 Identity has been reconciled and is no longer a blocker. Do not rewrite downstream domains to fix the former documentation mismatch.

Any future identity change must preserve:

- `users` as canonical account truth
- `roles` / `user_roles` as canonical authorization truth
- `students` as Student-domain truth
- `students.user_id → users.id` as the account/profile boundary
- the migration chain from `0001_identity` onward

## 2026-09-01 — Identity reconciliation

Decision:

Phase 2 Identity is complete and remains a separate domain from Student Profile. Identity owns accounts, authentication, roles, and account state; Student owns profile data.

Reason:

The current codebase already implements the correct foreign-key boundary (`students.user_id → users.id`). The inconsistency was primarily historical documentation plus a missing root migration/config compatibility issue. Correct those artifacts instead of coupling domains or rewriting working downstream features.

Impact:

- restored `0001_identity` migration
- added JWT expiration configuration required by existing security code
- aligned password validation with bcrypt's effective limit
- made role loading explicit
- updated Phase 2 documentation and roadmap status

---

# 33. Golden Rule

> **Build the smallest coherent system that can correctly perform the next step of the CareerLens decision journey.**

Do not build architecture for a hypothetical future when the current product requirement does not need it.

---

# 34. Source of Truth Hierarchy

When making decisions, use this order:

```text
1. Product requirements
2. This SOURCE_OF_TRUTH.md
3. Explicit architectural decisions recorded here
4. Current implementation
5. General engineering convention
6. Personal preference
```

If current code conflicts with this document, current code does not automatically win.

---

# 35. Final Product Mental Model

```text
                         CAREERLENS
                             │
                             ▼
                         PERSON
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
          Academic      Assessment      Interests
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                          Evidence
                             │
                             ▼
                     Career Intelligence
                             │
                             ▼
                     Recommendation
                    ┌────────┼────────┐
                    ▼        ▼        ▼
                  Score   Evidence  Confidence
                    │
                    ▼
                Skill Gaps
                    │
                    ▼
                Education
                    │
                    ▼
                Action Plan
                    │
                    ▼
               Human Review
                    │
                    ▼
                  Report

AI = assistance layer around this system.
```

---

## End of CareerLens Source of Truth

**This document is authoritative until explicitly superseded by a newer version.**
