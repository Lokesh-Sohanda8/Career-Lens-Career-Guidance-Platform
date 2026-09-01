# CareerLens — Source of Truth
## Current Phase: Clean Rebuild from Scratch

**Document Status:** Authoritative  
**Purpose:** This file is the single source of truth for rebuilding CareerLens in a new chat/repository.  
**Current Decision:** The previous implementation is **not** the architectural source of truth. We are restarting the product implementation from a clean foundation while preserving the validated product idea, philosophy, scope, and important decisions captured below.

---

# 1. Product Identity

## Product Name

**CareerLens**

## Product Category

AI + Human Career Intelligence and Career Counselling Platform.

## Core Idea

CareerLens is a career decision-support platform designed to help students and individuals understand:

- who they are
- what they are good at
- what they may be suited for
- which careers align with them
- what skills those careers require
- what education pathways lead toward those careers
- which colleges/programs may fit their situation
- what they should do next
- when human counselling is useful

The platform combines **structured evidence, assessments, career intelligence, education intelligence, human counselling, and AI assistance**.

---

# 2. The Core Product Philosophy

CareerLens should not simply answer:

> "Which career should I choose?"

It should help answer:

> "Why might this career fit me, what evidence supports that conclusion, what are the alternatives, what are the risks or gaps, and what should I do next?"

The product therefore focuses on **decision support**, not deterministic life prediction.

### Core principle

```text
Understand the person
        ↓
Collect evidence
        ↓
Interpret evidence
        ↓
Explore career options
        ↓
Compare alternatives
        ↓
Build an education path
        ↓
Build an action plan
        ↓
Use human counselling where valuable
        ↓
Continuously reassess
```

---

# 3. The Problem We Are Solving

Career decisions are fragmented.

A student may have to use separate services for:

- psychometric testing
- career information
- college discovery
- entrance-exam information
- counselling
- skill planning
- course discovery
- career research

Parents may struggle to understand whether advice is reliable.

Counsellors may lack a unified evidence-based workspace.

Institutes may lack structured career-intelligence infrastructure.

CareerLens aims to bring these pieces into one coherent decision system.

---

# 4. Target Users

## Primary

### Students

Especially:

- school students
- higher-secondary students
- undergraduate students
- students considering a career change
- students unsure about their academic/career direction

## Secondary

### Parents

Parents need:

- understandable reports
- evidence behind recommendations
- education options
- career alternatives
- financial/location considerations
- ability to participate without dominating the student's decision

### Human Counsellors

Counsellors need:

- student profiles
- assessment results
- evidence
- career candidates
- education options
- session notes
- recommendation history
- ability to review and override recommendations

### Educational Institutions / Career Institutes

Potential future customers:

- schools
- colleges
- coaching institutes
- counselling organizations
- education companies

---

# 5. Product Differentiation

The intended differentiation is not one feature.

It is the combination of multiple intelligence layers.

```text
                 CAREERLENS
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Psychometric     Academic       Interest &
 Intelligence     Evidence      Preference
      │              │              │
      └──────────────┼──────────────┘
                     ▼
             Career Intelligence
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Skills       Education     Human
     & Gaps       Pathways    Counselling
        │            │            │
        └────────────┼────────────┘
                     ▼
              Career Decision
                     │
                     ▼
             Personalized Plan
```

Later, additional exploratory layers may include:

- neuroscience/cognitive signals
- traditional counselling methods
- palmistry as an explicitly exploratory/non-scientific experience

These must not be represented as scientifically validated predictors when they are not.

---

# 6. Evidence Hierarchy

CareerLens must distinguish between different kinds of information.

## Tier 1 — Strongest decision evidence

Examples:

- validated assessment results
- academic performance
- documented skills
- verified preferences
- user-provided goals
- verified education data
- verified career requirements
- counsellor observations

## Tier 2 — Contextual evidence

Examples:

- interests
- constraints
- financial preferences
- location preferences
- learning preferences
- previous experiences

## Tier 3 — Exploratory / reflective inputs

Examples:

- traditional methods
- symbolic frameworks
- palmistry

These may be used for reflection or engagement, but must not silently become authoritative evidence.

---

# 7. Product Output Philosophy

CareerLens should avoid presenting recommendations as absolute truths.

Bad:

> "You are definitely meant to become a Data Scientist."

Better:

> "Data Science currently appears to be a strong-fit option based on your assessment profile, academic evidence, interests and skill alignment."

A recommendation should expose:

- recommendation
- score
- confidence
- supporting evidence
- reasons
- limitations
- alternative careers
- skill gaps
- next actions

---

# 8. Current Product Journey

The first complete product journey should be:

```text
User Registration
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
Career Compatibility Scoring
       ↓
Top Career Options
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
Final Career Guidance Report
```

This is the **core MVP journey**.

---

# 9. MVP Scope

The first implementation must NOT attempt to build the entire long-term vision.

## MVP must include

### Identity & Access

- registration
- login
- authentication
- user roles
- student profile

### Student Intelligence

- academic profile
- interests
- preferences
- goals
- constraints

### Assessment

- assessment catalog
- assessment questions
- assessment sessions
- responses
- scoring
- normalized traits
- assessment result

### Career Intelligence

- career catalog
- career categories
- career descriptions
- career requirements
- career-to-skill relationships
- career-to-education relationships
- career compatibility scoring
- career ranking
- recommendation explanations

### Skill Intelligence

- skill catalog
- required skills
- student skills
- skill gaps
- priority

### Education Intelligence

- institutions
- programs/courses
- career-program relationships
- admission exams
- eligibility rules
- student education preferences

### Learning Path

- learning resources
- skill-to-resource relationships
- learning paths
- learning milestones
- user progress

### Human Counselling

- counsellor profiles
- counselling cases
- counselling sessions
- counsellor observations
- recommendation review
- counsellor override/confirmation

### Reporting

- career recommendation report
- evidence summary
- action plan
- counselling summary

---

# 10. Explicitly NOT MVP

Do not start with these.

- multi-agent AI architecture
- complex autonomous agents
- advanced RAG
- model orchestration
- complicated microservices
- real-time collaboration
- marketplace
- subscriptions/payments
- advanced analytics
- institute SaaS
- mobile applications
- large-scale data pipelines
- sophisticated ML admission prediction
- palmistry automation
- neuroscience inference
- massive external integrations

These belong to later phases.

---

# 11. Architecture Decision

## Start as a Modular Monolith

The initial backend should be:

```text
FastAPI
+
PostgreSQL
+
SQLAlchemy
+
Alembic
+
Pydantic
```

Do NOT begin with microservices.

The system should have clear domain boundaries internally so that services can be extracted later if necessary.

---

# 12. High-Level Architecture

```text
                        CareerLens
                            │
                ┌───────────┴───────────┐
                │                       │
             Frontend                Backend
                                        │
                              ┌─────────┴─────────┐
                              │                   │
                         API Layer           Domain Layer
                              │                   │
                              │       ┌───────────┼───────────┐
                              │       ▼           ▼           ▼
                              │    Identity    Profile    Assessment
                              │
                              │       ▼           ▼           ▼
                              │     Career      Skills     Education
                              │
                              │       ▼           ▼           ▼
                              │   Counselling Learning   Reporting
                              │
                              └───────────┬───────────────┘
                                          ▼
                                      PostgreSQL
```

---

# 13. Backend Domain Boundaries

The clean rebuild should use a deliberately small number of meaningful domains.

## 13.1 Identity

Responsibilities:

- users
- authentication
- roles
- account state

---

## 13.2 Student Profile

Responsibilities:

- student identity/profile
- academic information
- interests
- preferences
- goals
- constraints

---

## 13.3 Assessments

Responsibilities:

- assessment definitions
- dimensions/traits
- questions
- options
- assessment sessions
- responses
- scoring
- results

---

## 13.4 Career Intelligence

Responsibilities:

- careers
- career categories
- career requirements
- career evidence
- career compatibility
- career ranking
- recommendation explanations

This is the **core intelligence domain**.

---

## 13.5 Skills

Responsibilities:

- skills
- skill categories
- career-required skills
- student skill evidence
- skill gaps
- skill priority

---

## 13.6 Education

Responsibilities:

- institutions
- programs
- courses
- career-program relationships
- admission exams
- eligibility rules
- education preferences

---

## 13.7 Learning

Responsibilities:

- resources
- learning paths
- milestones
- prerequisites
- user progress

---

## 13.8 Counselling

Responsibilities:

- counsellors
- counselling cases
- sessions
- counsellor observations
- recommendation review
- human decisions
- overrides

---

## 13.9 Recommendations

Responsibilities:

- recommendation runs
- recommendation snapshots
- evidence aggregation
- scores
- confidence
- explanation
- recommendation history

This should consume intelligence from other domains rather than owning their data.

---

## 13.10 Reports

Responsibilities:

- report generation
- report snapshots
- report sections
- export formats

---

# 14. AI Is a Layer, Not the Foundation

AI should NOT own core business truth.

The architecture should be:

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

Not:

```text
User
 ↓
LLM
 ↓
Whatever the model says
```

AI may eventually help with:

- conversational career guidance
- explanations
- report drafting
- counsellor assistance
- question generation
- resource summaries
- personalized learning explanations
- research assistance

But canonical facts must come from structured data.

---

# 15. Recommendation Engine

This is the most important future engine.

Conceptually:

```text
Student
  │
  ├── Academic evidence
  ├── Assessment evidence
  ├── Interest evidence
  ├── Preference evidence
  ├── Skill evidence
  ├── Goal evidence
  └── Constraints
          │
          ▼
   Feature Normalization
          │
          ▼
   Candidate Generation
          │
          ▼
   Career Compatibility
          │
          ▼
      Ranking
          │
          ▼
 Evidence-backed Results
```

A recommendation must be reproducible.

Every recommendation run should ideally record:

- engine version
- input snapshot/version
- factors used
- factor weights
- candidate careers
- scores
- evidence
- confidence
- timestamp

---

# 16. Recommendation Score

The exact mathematical formula is NOT fixed yet.

The implementation must therefore avoid hardcoding arbitrary weights before the product logic is finalized.

A conceptual model:

```text
Career Score =
    Assessment Alignment
  + Academic Alignment
  + Interest Alignment
  + Skill Alignment
  + Goal Alignment
  + Preference Alignment
  + Constraint Compatibility
```

Weights must be configurable/versioned rather than scattered across application code.

---

# 17. College Predictor

The college predictor must evolve in stages.

## Version 1

Fit-based matching:

```text
Career relevance
+
Program relevance
+
Location
+
Budget
+
Study mode
```

## Later

Eligibility:

```text
Academic requirements
+
Subjects
+
Entrance exams
+
Category/reservation rules
+
Other eligibility conditions
```

## Later still

Probabilistic admission prediction:

```text
Historical cutoffs
+
Seats
+
Applicant profile
+
Exam performance
+
Year-wise distributions
+
Other validated features
```

Until sufficient data exists, do NOT claim an admission probability.

---

# 18. Human Intelligence

Human counselling is not a decorative add-on.

The intended model is:

```text
AI / Structured Intelligence
            ↓
     Preliminary Analysis
            ↓
       Human Counsellor
            ↓
 Review / Challenge / Add Context
            ↓
      Final Guidance
```

A counsellor should be able to:

- review evidence
- add observations
- challenge a recommendation
- confirm a recommendation
- reject a recommendation
- add contextual information
- create a final guidance outcome

Human decisions should be stored separately from automated scores.

---

# 19. Evidence Model

A generic evidence abstraction should eventually support:

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

Possible sources:

- assessment
- academic record
- profile
- skill evidence
- counsellor
- education data
- user preference

This creates an auditable recommendation system.

---

# 20. Data Governance

Career guidance can influence major life decisions.

Therefore the system must prioritize:

- transparency
- explainability
- privacy
- auditability
- versioning
- source tracking
- human review
- user control

The system should never imply certainty where uncertainty exists.

---

# 21. Traditional Methods, Palmistry & Neuroscience

These are part of the broader product vision but require careful positioning.

## Neuroscience / Cognitive Layer

Potential future use:

- cognitive-task signals
- cognitive profile experiments
- attention/memory/task performance research

Do not make unsupported medical or neurological claims.

## Traditional Methods

May be used as:

- reflective frameworks
- cultural approaches
- counselling prompts

## Palmistry

May be offered as:

- exploratory
- entertainment
- reflective

It should not be represented as scientifically validated career prediction.

---

# 22. API Philosophy

Use REST APIs initially.

Example structure:

```text
/api/v1/auth
/api/v1/users
/api/v1/students
/api/v1/assessments
/api/v1/careers
/api/v1/skills
/api/v1/education
/api/v1/learning
/api/v1/counselling
/api/v1/recommendations
/api/v1/reports
```

Avoid creating separate API modules for every tiny concept.

---

# 23. Domain Structure Philosophy

Each meaningful domain should follow a consistent structure.

Example:

```text
domain/
├── __init__.py
├── models.py
├── schemas.py
├── repository.py
├── service.py
└── events.py        # only when actually needed
```

API:

```text
api/v1/
└── <domain>.py
```

Do not create five layers of abstraction before there is a real need.

---

# 24. Database Philosophy

PostgreSQL is the system of record.

Use:

- UUID identifiers
- foreign keys
- unique constraints
- indexes
- timestamps
- soft-delete/active state where appropriate
- audit fields where required
- migration versioning

Do not use JSON as a replacement for proper relational modeling when the data has stable structure or relationships.

JSON is appropriate for:

- flexible metadata
- versioned configuration
- extensible assessment metadata
- external provider payloads
- experimental data

---

# 25. Version Everything That Affects Recommendations

At minimum:

```text
Assessment Version
Scoring Version
Career Data Version
Recommendation Engine Version
Education Data Version
College Predictor Version
Report Version
```

This allows:

```text
"What did CareerLens know and why did it recommend this career at that time?"
```

to be answered later.

---

# 26. Testing Philosophy

Every domain should eventually have:

### Unit tests

For:

- scoring
- validation
- business rules
- ranking
- eligibility

### Integration tests

For:

- database operations
- API endpoints
- authentication
- domain interactions

### End-to-end test

At least one complete journey:

```text
Register
 ↓
Create Student Profile
 ↓
Complete Assessment
 ↓
Generate Career Recommendations
 ↓
View Evidence
 ↓
View Skill Gaps
 ↓
View Education Options
 ↓
Create Learning Path
 ↓
Counsellor Review
 ↓
Generate Report
```

This journey is more important than having hundreds of isolated endpoints.

---

# 27. Production Readiness Principles

From the first implementation:

- environment-based configuration
- secrets outside source code
- structured logging
- request IDs
- consistent error responses
- validation
- database migrations
- transaction boundaries
- authentication
- authorization
- rate limiting where required
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

But do not implement infrastructure complexity merely for appearance.

---

# 28. Observability

Eventually capture:

```text
Request
 ↓
Domain operation
 ↓
Recommendation run
 ↓
Evidence sources
 ↓
AI call (if any)
 ↓
Response
```

Important metrics:

- latency
- errors
- recommendation generation time
- AI token/cost usage
- AI failures
- recommendation acceptance/rejection
- counsellor overrides

---

# 29. Initial Build Order

This is the authoritative build sequence for the clean rebuild.

## Phase 1 — Foundation

```text
1. Repository structure
2. Environment configuration
3. FastAPI application
4. PostgreSQL connection
5. SQLAlchemy setup
6. Alembic
7. Base models
8. Error handling
9. Logging
10. Health/readiness
11. Configuration
12. Testing foundation
```

## Phase 2 — Identity

```text
13. Users
14. Authentication
15. Roles
16. Student identity
```

## Phase 3 — Student Profile

```text
17. Student profile
18. Academic records
19. Interests
20. Preferences
21. Goals
22. Constraints
```

## Phase 4 — Assessment

```text
23. Assessment definitions
24. Dimensions
25. Questions
26. Options
27. Sessions
28. Responses
29. Scoring
30. Results
```

## Phase 5 — Career Intelligence

```text
31. Career catalog
32. Career categories
33. Career requirements
34. Career-skill mapping
35. Career-education mapping
36. Candidate generation
37. Compatibility scoring
38. Ranking
39. Evidence explanation
```

## Phase 6 — Skill Intelligence

```text
40. Skills
41. Student skill evidence
42. Skill gaps
43. Skill priorities
```

## Phase 7 — Recommendation Engine

```text
44. Recommendation run
45. Evidence aggregation
46. Score calculation
47. Confidence
48. Recommendation snapshot
49. Recommendation history
```

## Phase 8 — Education

```text
50. Institutions
51. Programs
52. Program-career relationships
53. Admission exams
54. Eligibility rules
55. Education preferences
56. Program matching
```

## Phase 9 — Learning

```text
57. Resources
58. Resource-skill relationships
59. Learning paths
60. Milestones
61. Progress
```

## Phase 10 — Human Counselling

```text
62. Counsellors
63. Cases
64. Sessions
65. Observations
66. Recommendation review
67. Human override
68. Final guidance
```

## Phase 11 — Reports

```text
69. Recommendation report
70. Evidence report
71. Career action plan
72. Counsellor report
```

## Phase 12 — AI

Only after the deterministic product works:

```text
73. AI career assistant
74. AI explanations
75. AI report drafting
76. Counsellor copilot
77. RAG
78. AI guardrails
79. AI evaluation
80. AI observability
```

---

# 30. What We Are NOT Doing in the New Chat

Do not carry forward architectural complexity from the previous implementation just because it already exists.

Do not begin with:

- dozens of placeholder domains
- empty AI agent folders
- microservice boundaries
- multiple overlapping intelligence domains
- duplicate API modules
- arbitrary migrations
- premature event-driven architecture
- premature Redis infrastructure
- complex orchestration

Start with a small number of coherent domains.

---

# 31. Clean-Rebuild Rule

The new implementation must answer three questions for every feature:

### 1. What problem does this solve?

### 2. Which domain owns it?

### 3. What data is the source of truth?

If those cannot be answered clearly, the feature should not be implemented yet.

---

# 32. Current Development Philosophy

We build vertically, not horizontally.

Bad approach:

```text
Build 80 database tables
↓
Build 100 APIs
↓
Build AI
↓
Hope everything connects
```

Preferred approach:

```text
Student
 ↓
Profile
 ↓
Assessment
 ↓
Career Recommendation
 ↓
Skill Gap
 ↓
Education
 ↓
Counsellor
 ↓
Report
```

Build this journey end-to-end first.

Then expand.

---

# 33. First Vertical Slice

The first real milestone is:

## "Student → Assessment → Career Recommendation"

It should work completely.

### Input

```text
Student Profile
+
Academic Information
+
Interests
+
Assessment Responses
```

### Processing

```text
Assessment Scoring
        ↓
Normalized Profile
        ↓
Career Candidate Generation
        ↓
Career Compatibility
        ↓
Ranking
```

### Output

```text
Top Career Options
+
Scores
+
Reasons
+
Evidence
+
Confidence
+
Alternative Careers
```

No LLM is required for this first slice.

---

# 34. Definition of Done for the First Slice

The first slice is complete only when:

- a real user can authenticate
- a student profile can be created
- an assessment can be completed
- responses are stored
- scoring works
- results are persisted
- careers exist in the database
- career requirements exist
- compatibility can be calculated
- recommendations are persisted
- the API returns explainable results
- automated tests cover the critical path
- the database can be recreated using migrations
- the entire flow can be demonstrated locally

---

# 35. Long-Term Product Vision

Eventually CareerLens can become:

```text
                    CAREERLENS
                        │
                        ▼
              Personal Career Graph
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
      Person          Career          Education
        │               │                │
        ▼               ▼                ▼
    Assessments       Skills          Colleges
    Interests        Requirements     Programs
    Academics        Pathways         Exams
    Cognition        Outcomes         Eligibility
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                Recommendation Engine
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        AI Assistance         Human Counselling
             │                     │
             └──────────┬──────────┘
                        ▼
                Career Decision
                        │
                        ▼
                  Action Plan
                        │
                        ▼
                Continuous Growth
```

---

# 36. One-Sentence Product Definition

> **CareerLens is an evidence-driven career intelligence platform that combines assessments, personal context, career and education intelligence, AI assistance, and human counselling to help people make better-informed career decisions and act on them.**

---

# 37. The Rule for the New Chat

When starting the new implementation chat, provide this file first and state:

> **"This is the source of truth. Ignore the previous CareerLens implementation architecture. Rebuild the product from scratch according to this document. Do not introduce new domains, infrastructure or complexity unless justified against this source of truth."**

The new chat should treat this document as the baseline and build incrementally from Phase 1.

---

# 38. Current Status

```text
PRODUCT IDEA              ✅ Defined
PRODUCT PHILOSOPHY        ✅ Defined
TARGET USERS              ✅ Defined
MVP                       ✅ Defined
CORE JOURNEY              ✅ Defined
ARCHITECTURE DIRECTION    ✅ Defined
DOMAIN BOUNDARIES         ✅ Defined
BUILD ORDER               ✅ Defined

CLEAN IMPLEMENTATION      ⏳ Not started
FIRST VERTICAL SLICE      ⏳ Not started
PRODUCTION DEPLOYMENT     ⏳ Later
AI LAYER                  ⏳ Later
ADVANCED PREDICTION       ⏳ Later
```

## Current phase

# **CLEAN REBUILD — PHASE 1: FOUNDATION**

The next implementation task is **not** to build every module.

It is to create a clean, runnable, testable backend foundation and then build the first vertical slice.
