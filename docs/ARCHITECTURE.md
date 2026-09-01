# CareerLens Architecture — Phase 1

## Architectural decision

CareerLens starts as a modular monolith. The backend is FastAPI + PostgreSQL + SQLAlchemy + Alembic + Pydantic.

## Boundary rules

1. API modules own HTTP concerns.
2. Domain services own business workflows.
3. Repositories own persistence operations.
4. SQLAlchemy models represent persisted state.
5. Pydantic schemas represent API/service contracts.
6. PostgreSQL is the system of record.
7. AI is an assistance layer, not the source of canonical business truth.
8. New domains are added only when their ownership is clear.
9. Do not introduce microservices, agents, RAG, Redis, event buses, or orchestration without a justified product need.

## Phase 1 dependency direction

```text
API -> Core / DB
DB  -> Core
Core -> no application layer
```

As domains arrive:

```text
API -> Domain Service -> Repository -> DB
API -> Domain Schema
Domain Model -> DB Base
```

Avoid domain code importing API routers.

## Request flow

```text
HTTP Request
   |
   v
Request ID Middleware
   |
   v
API Router
   |
   v
Domain Service
   |
   v
Repository
   |
   v
PostgreSQL
```

## Health semantics

`/api/v1/health` means the process is alive.

`/api/v1/ready` means the process can reach PostgreSQL.
