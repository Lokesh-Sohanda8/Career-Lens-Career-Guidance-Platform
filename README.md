# CareerLens

> **AI + Human Career Intelligence and Career Counselling Platform**

**Current Phase:** Phase 12 — AI Intelligence
**Architecture Authority:** [`source_of_truth.md`](./source_of_truth.md)
**Architecture:** Modular Monolith
**Backend:** FastAPI + PostgreSQL + SQLAlchemy + Alembic
**Status:** Active Development

---

## 1. What is CareerLens?

CareerLens is an evidence-driven career intelligence platform designed to help students and career seekers make better-informed career decisions.

It combines:

* Student profiles
* Academic information
* Interests and preferences
* Psychometric assessments
* Career intelligence
* Skill intelligence
* Career recommendations
* Education and program matching
* Learning paths
* Counselling workflows
* Structured reports
* AI-powered career assistance

CareerLens is designed as a **decision-support system**, not a system that claims to predict a person's future.

The platform should help answer:

> **Why might this career fit me?**

> **What evidence supports that recommendation?**

> **What alternatives should I consider?**

> **What skill gaps do I have?**

> **Which education pathways are relevant?**

> **What should I do next?**

> **When should I involve a human counsellor?**

---

# 2. Architecture Authority

The most important file in this repository is:

```text
source_of_truth.md
```

This is **The Bible of CareerLens**.

It contains the authoritative:

* Product definition
* Architecture
* Domain boundaries
* Database rules
* API conventions
* Security rules
* AI architecture
* Versioning rules
* Phase status
* Architectural decisions
* Definition of Done
* Recovery instructions

### Rule

If the implementation and `source_of_truth.md` disagree:

1. Identify the disagreement.
2. Determine whether the change was intentional.
3. If intentional, update `source_of_truth.md`.
4. If unintentional, fix the implementation.
5. Never allow silent architectural drift.

### Recovery rule

If the codebase becomes confusing, incomplete, corrupted, or partially rebuilt:

> **Reconstruct the system from `source_of_truth.md`, not from the existing code.**

The code is the implementation.

The Bible is the architectural intent.

---

# 3. Current Product Architecture

CareerLens is being built as a **modular monolith**.

```text
Frontend
    │
    ▼
REST / JSON
    │
    ▼
FastAPI
    │
    ├── API Layer
    │
    ├── Core Infrastructure
    │
    ├── Domain Services
    │
    └── Repositories
            │
            ▼
        SQLAlchemy
            │
            ▼
        PostgreSQL
```

AI sits above the deterministic intelligence layer:

```text
Canonical Data
      │
      ▼
Deterministic Intelligence
      │
      ▼
Evidence Aggregation
      │
      ▼
Recommendation Engine
      │
      ▼
AI Assistance
```

CareerLens must **never** become:

```text
User
  │
  ▼
LLM
  │
  ▼
Business Truth
```

---

# 4. Current Product Journey

The intended product journey is:

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
    ↓
AI Assistance
```

---

# 5. Current Domains

CareerLens currently follows these domain boundaries:

```text
backend/app/domains/

├── identity/
├── student/
├── assessments/
├── careers/
├── skills/
├── recommendations/
├── education/
├── learning/
├── counselling/
├── reports/
└── ai/
```

## Domain ownership

| Domain          | Responsibility                                                              |
| --------------- | --------------------------------------------------------------------------- |
| Identity        | Users, authentication, roles, account state                                 |
| Student         | Profile, academics, interests, preferences, goals, constraints              |
| Assessments     | Assessment definitions, questions, sessions, responses, results             |
| Careers         | Career catalog, categories, requirements                                    |
| Skills          | Skills, career-skill requirements, student skill evidence, gaps             |
| Recommendations | Recommendation runs, scoring, evidence, ranking, snapshots                  |
| Education       | Institutions, programs, exams, eligibility                                  |
| Learning        | Resources, learning paths, milestones, progress                             |
| Counselling     | Counselling workflow, sessions, notes, decisions, actions, goals            |
| Reports         | Structured reports, snapshots, sections, exports                            |
| AI              | AI assistance, context building, guardrails, provider integration, AI audit |

### Ownership rule

A domain owns its **canonical data**.

Other domains may consume that data, but should not silently duplicate ownership.

---

# 6. Identity and Student Boundary

Identity and Student Profile are intentionally separate.

```text
             IDENTITY
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
     Users     Roles   User Roles
                │
                │
                ▼
             STUDENT
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
    Profile  Academics  Interests
                │
                ├── Preferences
                ├── Goals
                └── Constraints
```

Identity owns:

```text
users
roles
user_roles
authentication
account state
```

Student owns:

```text
students
academic_records
student_interests
student_preferences
student_goals
student_constraints
```

The relationship is:

```text
students.user_id → users.id
```

Registration creates an account and assigns the server-controlled `student` role.

It does **not** automatically create a completed student profile.

This separation was explicitly reconciled in Phase 2 and is now part of the canonical architecture.

---

# 7. Backend Structure

The backend follows a modular structure:

```text
backend/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   ├── dependencies.py
│   │   └── v1/
│   │       ├── router.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── students.py
│   │       ├── assessments.py
│   │       ├── careers.py
│   │       ├── skills.py
│   │       ├── recommendations.py
│   │       ├── education.py
│   │       ├── learning.py
│   │       ├── counselling.py
│   │       ├── reports.py
│   │       ├── ai.py
│   │       └── health.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── ...
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── models.py
│   │   └── session.py
│   │
│   └── domains/
│       ├── identity/
│       ├── student/
│       ├── assessments/
│       ├── careers/
│       ├── skills/
│       ├── recommendations/
│       ├── education/
│       ├── learning/
│       ├── counselling/
│       ├── reports/
│       └── ai/
│
├── migrations/
│   └── versions/
│
├── tests/
│
├── .env.example
├── pyproject.toml
├── requirements.txt
└── Dockerfile
```

Individual domains normally follow:

```text
domain/
├── __init__.py
├── models.py
├── schemas.py
├── repository.py
└── service.py
```

Additional files should only be introduced when an actual domain requirement justifies them.

---

# 8. API Convention

All APIs are versioned.

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
/api/v1/recommendations
/api/v1/education
/api/v1/learning
/api/v1/counselling
/api/v1/reports
/api/v1/ai
```

Infrastructure endpoints include:

```text
GET /api/v1/health
GET /api/v1/ready
```

API modules should represent meaningful product capabilities rather than every individual database table.

---

# 9. Database

PostgreSQL is the system of record.

SQLAlchemy is used as the ORM.

Alembic manages schema migrations.

### Database principles

Use:

* UUID identifiers
* Foreign keys
* Unique constraints
* Appropriate indexes
* Timestamps
* Audit fields where required
* Active/soft-delete state where appropriate
* Alembic migrations

Use JSON only when the data is genuinely flexible, such as:

* Metadata
* Versioned configuration
* Assessment metadata
* External provider payloads
* Experimental data

Do not use JSON simply to avoid proper relational modeling.

---

# 10. Migration Architecture

Migrations form a dependency chain.

The current conceptual order is:

```text
0001 Identity
    ↓
0002 Student Profile
    ↓
0003 Assessment
    ↓
0004 Careers
    ↓
0005 Skills
    ↓
0006 Recommendations
    ↓
0007 Education
    ↓
0008 Learning
    ↓
0009 Counselling
    ↓
0010 Reports
    ↓
0011 AI
```

The Identity migration is the root of the current domain migration chain.

Never casually rewrite historical migrations after they have become part of the canonical rebuild history.

---

# 11. AI Architecture

Phase 12 introduces the first AI layer.

AI is deliberately implemented as an **assistance layer**.

```text
Canonical CareerLens Data
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
       AI Model
          │
          ▼
      AI Response
          │
          ▼
   Interaction Audit
```

## Current AI capabilities

The current foundation provides:

* Provider abstraction
* OpenAI-compatible provider
* Structured student context
* Context versioning
* Prompt versioning
* Basic guardrails
* AI interaction auditing
* Input hashing
* Provider error handling
* Authenticated student ownership

Current endpoints:

```text
POST /api/v1/ai/ask
GET  /api/v1/ai/interactions
```

AI is disabled by default.

```env
AI_ENABLED=false
```

---

# 12. AI Rules

AI must never become the canonical source of truth.

AI may:

* Explain
* Summarize
* Compare
* Suggest
* Assist counsellors
* Help interpret structured CareerLens information

AI must not:

* Invent student facts
* Fabricate eligibility requirements
* Guarantee career outcomes
* Replace deterministic recommendations
* Silently modify canonical domain data
* Reveal hidden instructions
* Diagnose health or mental-health conditions
* Treat missing information as confirmed facts

Important education, eligibility, admission, or regulatory information should be verified against the appropriate official source.

---

# 13. AI Provider Abstraction

CareerLens should not be tightly coupled to one model vendor.

The architecture is:

```text
AIService
    │
    ▼
Provider Abstraction
    │
    ├── OpenAI-compatible provider
    ├── Future providers
    └── Future local models
```

The current provider configuration is environment-based:

```env
AI_ENABLED=false
AI_PROVIDER=openai_compatible
AI_BASE_URL=https://api.openai.com/v1
AI_API_KEY=
AI_MODEL=gpt-5-mini
AI_TIMEOUT_SECONDS=30
```

Provider-specific implementation should remain isolated from domain business logic.

---

# 14. AI Auditability

AI interactions are recorded in:

```text
ai_interactions
```

The audit record includes:

```text
student
task_type
provider
model
prompt_version
context_version
input_hash
response
status
latency
error_code
timestamp
```

Raw prompt/context is not persisted by default.

This allows AI behavior to remain traceable while avoiding unnecessary persistence of the complete student context.

---

# 15. Recommendations

The recommendation engine is deterministic first.

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

Recommendations must remain explainable and auditable.

They should not be presented as absolute truths.

Important recommendation inputs and outputs must be versioned.

---

# 16. Reports

Reports are structured snapshots of CareerLens state.

They are **not** the canonical source of student data.

```text
Student Data
     +
Assessment
     +
Recommendations
     +
Skills
     +
Education
     +
Learning
     +
Counselling
     ↓
Report Snapshot
```

Historical reports should remain auditable even if the underlying student data changes later.

PDF/document rendering is intentionally separated from report storage.

---

# 17. Counselling

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

Human decisions must remain distinguishable from automated scores.

Counsellors may review, challenge, confirm, reject, or override automated recommendations.

---

# 18. Security

Security is a first-class requirement.

Rules include:

* Never store plaintext passwords.
* Never log passwords.
* Never return password hashes.
* Keep JWT secrets outside source control.
* Use environment variables for secrets.
* Validate authentication before protected operations.
* Enforce authorization explicitly.
* Never trust role information supplied by clients.
* Use HTTPS in deployed environments.
* Keep authentication behind the Identity domain.

Passwords are bcrypt-hashed.

JWT authentication uses bearer tokens.

The JWT stores the authenticated user UUID in `sub` and uses configured expiration.

---

# 19. Configuration

Environment-specific configuration belongs in environment variables.

Example:

```env
APP_NAME=CareerLens API
APP_VERSION=0.1.0
ENVIRONMENT=development
DEBUG=false

DATABASE_URL=postgresql+asyncpg://careerlens:careerlens@localhost:5432/careerlens

LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:3000

SECRET_KEY=change-me-in-development
ALGORITHM=HS256

AI_ENABLED=false
AI_PROVIDER=openai_compatible
AI_BASE_URL=https://api.openai.com/v1
AI_API_KEY=
AI_MODEL=gpt-5-mini
AI_TIMEOUT_SECONDS=30
```

Never commit real secrets.

Use:

```text
.env
```

for local secrets.

Use:

```text
.env.example
```

for documented configuration.

---

# 20. Local Development

## Prerequisites

Recommended:

* Python 3.11+
* PostgreSQL 15+
* Docker Desktop
* Git

Docker is the preferred local development path.

---

## Start with Docker

From the repository root:

```bash
docker compose up --build
```

This starts the local development environment.

---

## API

Once running:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
GET /api/v1/health
```

Readiness check:

```text
GET /api/v1/ready
```

---

# 21. Local Python Development

From `backend/`:

### Create virtual environment

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

### Install dependencies

Using the project configuration:

```bash
pip install -e ".[dev]"
```

Or using the reference dependency file:

```bash
pip install -r requirements.txt
```

> `pyproject.toml` is the primary dependency/configuration source.
> `requirements.txt` is maintained as a convenient reference dependency list.

---

# 22. Environment Setup

Copy the example environment file:

### Windows

```powershell
copy .env.example .env
```

### macOS/Linux

```bash
cp .env.example .env
```

Update the values as required for your local environment.

---

# 23. Run the API

From `backend/`:

```bash
uvicorn app.main:app --reload
```

The development server will normally be available at:

```text
http://localhost:8000
```

---

# 24. Database Migrations

Check the current migration state:

```bash
alembic current
```

Upgrade to the latest schema:

```bash
alembic upgrade head
```

Create a migration only after an actual schema change:

```bash
alembic revision --autogenerate -m "describe the change"
```

Then:

```bash
alembic upgrade head
```

Do not create arbitrary migrations simply to create files.

Every migration must represent a real schema change.

---

# 25. Testing

Run the complete test suite:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

The testing strategy consists of:

### Unit tests

Test:

* Validation
* Business rules
* Scoring
* Ranking
* Eligibility
* Security primitives
* AI guardrails
* AI context behavior

### Integration tests

Test:

* Database operations
* Authentication
* APIs
* Domain interactions

### E2E

Maintain at least one complete product journey from:

```text
Registration
    ↓
Profile
    ↓
Assessment
    ↓
Recommendation
    ↓
Education
    ↓
Learning
    ↓
Counselling
    ↓
Report
    ↓
AI Assistance
```

---

# 26. Development Philosophy

CareerLens follows a **vertical slice strategy**.

Do not build:

```text
100 tables
    ↓
100 APIs
    ↓
AI
    ↓
Try to connect everything
```

Instead build:

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

Every feature should be integrated before moving unnecessarily deep into another subsystem.

---

# 27. Current Phase Status

```text
Phase 1  — Foundation              ✅
Phase 2  — Identity                ✅ RECONCILED
Phase 3  — Student Profile         ✅
Phase 4  — Assessment              ✅
Phase 5  — Career Intelligence     ✅
Phase 6  — Skill Intelligence      ✅
Phase 7  — Recommendation Engine   ✅
Phase 8  — Education Intelligence  ✅
Phase 9  — Learning Intelligence   ✅
Phase 10 — Counselling              ✅
Phase 11 — Reports                 ✅
Phase 12 — AI Intelligence         🚧 CURRENT
```

### Phase 12 focus

The current phase establishes the AI foundation:

```text
AI Context
    ↓
Guardrails
    ↓
Provider Abstraction
    ↓
AI Response
    ↓
Auditability
```

Future AI work can build on this foundation.

---

# 28. Future AI Roadmap

Potential future capabilities include:

```text
AI Career Assistant
        ↓
AI Explanations
        ↓
AI Report Drafting
        ↓
Counsellor Copilot
        ↓
RAG
        ↓
Tool Calling
        ↓
Structured AI Actions
        ↓
Conversation Memory
        ↓
Model Routing
        ↓
Evaluation Harness
        ↓
Advanced Observability
```

These should be implemented incrementally.

Do not introduce multi-agent systems, complex orchestration, or RAG simply because they are technically interesting.

They must solve an actual product requirement.

---

# 29. Explicit Non-Goals

CareerLens is not currently intended to include:

* Microservices without a concrete need
* Autonomous multi-agent systems
* Large-scale RAG infrastructure
* Real-time collaboration
* Marketplace functionality
* Payments/subscriptions
* Institute SaaS
* Mobile applications
* Large-scale external integrations
* Guaranteed career prediction
* Admission probability prediction
* Medical or psychological diagnosis
* Unvalidated neuroscience inference
* Automated palmistry-based decisions

These may be reconsidered only through an explicit architectural/product decision.

---

# 30. Production Principles

Production readiness is built incrementally.

The project should maintain:

* Environment-based configuration
* Secret management
* Structured logging
* Request IDs
* Consistent error envelopes
* Input validation
* Authentication
* Authorization
* Health checks
* Readiness checks
* Database migrations
* Automated tests
* CI
* Linting
* Formatting
* Static checks
* Dependency management
* Security checks
* API versioning

Do not add infrastructure purely to make the repository look sophisticated.

---

# 31. Important Files

| File                       | Purpose                                           |
| -------------------------- | ------------------------------------------------- |
| `source_of_truth.md`       | **Authoritative architecture and product Bible**  |
| `README.md`                | Developer-facing project overview and setup guide |
| `backend/pyproject.toml`   | Primary Python project/dependency configuration   |
| `backend/requirements.txt` | Reference dependency list                         |
| `backend/.env.example`     | Environment configuration template                |
| `backend/app/main.py`      | FastAPI application entry point                   |
| `backend/app/api/`         | API routing layer                                 |
| `backend/app/core/`        | Cross-cutting infrastructure                      |
| `backend/app/db/`          | Database infrastructure/model registry            |
| `backend/app/domains/`     | Product domain implementations                    |
| `backend/migrations/`      | Database schema history                           |
| `backend/tests/`           | Automated tests                                   |
| `docs/`                    | Phase and implementation documentation            |

---

# 32. Working on a New Feature

Before implementing a feature:

### Step 1 — Read the Bible

```text
source_of_truth.md
```

### Step 2 — Identify the owning domain

Ask:

> Which domain owns this data?

### Step 3 — Define the vertical slice

```text
Model
 ↓
Schema
 ↓
Repository
 ↓
Service
 ↓
API
 ↓
Test
```

### Step 4 — Check dependencies

Do not create circular domain ownership.

### Step 5 — Implement

Follow the existing architecture.

### Step 6 — Test

Run:

```bash
pytest
```

### Step 7 — Update documentation

If the architecture changed:

```text
Update source_of_truth.md
```

Do not leave architectural decisions undocumented.

---

# 33. Rebuilding the Project From Scratch

If the repository is ever lost or needs a clean rebuild:

```text
1. Read source_of_truth.md
          ↓
2. Build Foundation
          ↓
3. Build Identity
          ↓
4. Build Student Profile
          ↓
5. Build Assessment
          ↓
6. Build Career Intelligence
          ↓
7. Build Skill Intelligence
          ↓
8. Build Recommendation Engine
          ↓
9. Build Education
          ↓
10. Build Learning
          ↓
11. Build Counselling
          ↓
12. Build Reports
          ↓
13. Build AI Intelligence
```

Never reconstruct the architecture from random implementation files.

The Bible is the recovery point.

---

# 34. Current Source of Truth

For the complete architecture, decisions, ownership rules, database structure, API conventions, phase definitions, and rebuild instructions, always refer to:

```text
source_of_truth.md
```

**Current version:**

```text
v12.1.0
```

**Current phase:**

```text
Phase 12 — AI Intelligence
```

---

# 35. Final Principle

CareerLens is being built around one central architectural principle:

```text
                 EVIDENCE
                    │
                    ▼
             STRUCTURED DATA
                    │
                    ▼
          DETERMINISTIC LOGIC
                    │
                    ▼
            HUMAN COUNSELLING
                    │
                    ▼
             AI ASSISTANCE
                    │
                    ▼
              BETTER DECISIONS
```

AI is powerful, but it is not the foundation.

The foundation is:

> **Structured evidence + deterministic intelligence + human judgement + responsible AI assistance.**

That is the architecture CareerLens is being built on.