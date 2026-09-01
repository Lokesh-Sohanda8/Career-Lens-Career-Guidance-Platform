# CareerLens
> **Current phase:** Phase 12 — AI Intelligence
> **Architecture authority:** [`source_of_truth.md`](./source_of_truth.md)

 — Phase 1 Foundation

This repository is the clean rebuild foundation for CareerLens.

## Scope

Phase 1 intentionally contains only the platform foundation:

- FastAPI application
- environment configuration
- PostgreSQL connection
- SQLAlchemy async setup
- Alembic migration setup
- request IDs
- structured application logging
- consistent error envelope
- health/readiness endpoints
- CORS configuration
- pytest foundation
- Docker Compose development environment

No business domains, AI agents, RAG, Redis, microservices, or recommendation logic are included yet.

## Architecture

```text
Frontend
   |
 REST/JSON
   v
FastAPI API
   |
   +-- core
   +-- db
   +-- api
   +-- domains (added incrementally)
   |
   v
PostgreSQL
```

## Local development

### 1. Start PostgreSQL and API

```bash
docker compose up --build
```

### 2. Check the API

- `GET /api/v1/health`
- `GET /api/v1/ready`
- `/docs`

### 3. Local Python setup without Docker

From `backend/`:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev]"
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

uvicorn app.main:app --reload
```

## Migrations

After adding the first domain model:

```bash
alembic revision --autogenerate -m "create identity tables"
alembic upgrade head
```

Do not create arbitrary migrations before there are actual schema changes.

## Tests

```bash
pytest
```

## Phase 1 definition of done

- application starts cleanly
- PostgreSQL connection is configured
- migrations are configured
- `/api/v1/health` works
- `/api/v1/ready` checks database readiness
- request IDs are returned
- unhandled errors use a safe error envelope
- tests execute
- Docker Compose can recreate the local environment

## Next phase

Phase 2 is Identity: users, authentication, roles, and student identity.
