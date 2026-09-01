# CareerLens — Phase 11: Reports

## Goal

Create an auditable reporting layer that captures structured CareerLens outputs as versioned student-owned snapshots.

## Architecture

```text
Profile
Assessment
Career Recommendation
Skills
Education
Learning
Counselling
      │
      ▼
 Structured Report Snapshot
      │
      ├── Report metadata
      └── Ordered sections
```

## Implemented

- report records
- report sections
- student ownership
- report version
- generation timestamp
- source snapshot
- ordered sections
- authenticated report retrieval
- report listing
- report creation
- migration
- unit coverage

## APIs

```text
GET  /api/v1/reports
GET  /api/v1/reports/{report_id}
POST /api/v1/reports
```

## Important boundary

Phase 11 stores structured report snapshots.

It does NOT:

- generate AI-written reports
- silently regenerate old reports
- treat a report as canonical domain truth
- predict admissions or career outcomes
- expose another student's reports
- introduce PDF rendering as a prerequisite for the reporting domain

A later presentation/export layer may render these snapshots to PDF or other formats.

## Versioning

Reports are snapshots. Changes to upstream data do not mutate an existing report.

A new report should be generated when a fresh snapshot is required.

## Ownership

Reports own report snapshots.

Career, Education, Skill, Learning, Counselling, and Student domains remain the canonical sources of their respective truth.
