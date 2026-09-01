# CareerLens — Phase 2: Identity (Reconciled)

## Status

**COMPLETE — reconciled against the Phase 12 codebase.**

## Purpose

Identity is the account and access boundary for CareerLens. It establishes who can access the platform and what role an account has.

```text
Account
  ↓
Register
  ↓
Student Role
  ↓
Login
  ↓
JWT
  ↓
Authenticated User
  ↓
Protected Domains
```

## Ownership

Identity owns only:

```text
users
roles
user_roles
authentication
account state
```

The Student Profile domain owns `students` and all student-profile data. Identity does **not** create or own the student profile row. The relationship is expressed by `students.user_id → users.id`.

This separation is intentional and is required by the current modular-monolith architecture.

## Canonical user

`users` contains:

- `id` — UUID primary key
- `email` — normalized, unique login identifier
- `password_hash` — bcrypt hash only
- `is_active` — account state
- `created_at`
- `updated_at`

## Roles

`roles` is the canonical role catalog.

Public registration assigns only:

```text
student
```

Privileged roles are not client-selectable. Role assignment belongs to trusted server-side workflows.

## Authentication

Current mechanism:

```text
OAuth2-compatible bearer token
JWT
```

JWT subject:

```text
sub = user UUID
```

JWT expiration is configured through `ACCESS_TOKEN_EXPIRE_MINUTES` and defaults to 60 minutes.

## Password boundary

The API accepts 8–72 character passwords because the current bcrypt implementation has a 72-byte effective input limit. Passwords are never returned or logged.

## APIs

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/users/me
```

## Protected-route flow

```text
Bearer Token
   ↓
JWT Decode
   ↓
Extract user UUID
   ↓
Load active User + Roles
   ↓
get_current_user
   ↓
Domain service
```

## Migration contract

Identity starts at:

```text
20260901_0001_identity
```

Then downstream migrations build on it:

```text
0001 Identity
   ↓
0002 Student Profile
   ↓
0003 Assessment
   ↓
...
   ↓
0011 AI
```

The root migration is mandatory. A rebuild must never delete it while keeping migrations that reference it.

## Reconciliation decision

Previous documentation described Phase 2 as inconsistent. That is now resolved. The correct architecture is:

```text
Identity
  └── User / Access / Roles
          │
          │ 1:1 ownership boundary
          ▼
Student
  └── Profile / Academic / Interest / Preference / Goal / Constraint
```

Identity and Student are separate domains. The foreign-key link is an integration boundary, not shared ownership.

## Exit criteria

- registration works
- duplicate email is rejected
- password is bcrypt-hashed
- student role is assigned server-side
- login returns JWT
- JWT expires
- invalid credentials are rejected
- inactive users are rejected
- protected routes reject missing/invalid tokens
- `/users/me` returns identity and roles
- root identity migration exists
- migration chain reaches current head
- security-critical unit tests exist
