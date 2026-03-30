# Construction OS v2 — VKG Audit Scoring L0 to L3

## Authority

Armand Lefebvre, L0 — Lefebvre Design Solutions LLC

## Purpose

Defines how Construction OS v2 actions are scored against the
ValidKernel Governance L0-L3 ring structure.

## Scoring Matrix

### L0 — Governance Context

| Check | Weight | Criteria |
|-------|--------|----------|
| Authority declared | Required | Command names issuing authority |
| Command ID present | Required | Unique document ID assigned |
| Date present | Required | ISO date assigned |
| Risk class declared | Required | RC1-RC4 assigned |
| Scope defined | Required | Explicit scope statement |

### L1 — Mission Directive

| Check | Weight | Criteria |
|-------|--------|----------|
| Objective stated | Required | Clear objective sentence |
| Required outcomes listed | Required | Enumerated outcomes |
| Constraints listed | Required | Explicit constraints |
| Non-goals listed | Required | Explicit non-goals |

### L2 — Deterministic Commit Gate

| Check | Weight | Criteria |
|-------|--------|----------|
| Checklist present | Required | All items enumerated |
| Gate rule defined | Required | ANY NO = HALT or equivalent |
| All items evaluable | Required | No ambiguous items |

### L3 — Capability Bound

| Check | Weight | Criteria |
|-------|--------|----------|
| TOUCH-ALLOWED defined | Required | Explicit list |
| NO-TOUCH defined | Required | Explicit list |
| Enforcement mode declared | Required | FAIL_CLOSED or equivalent |

## Scoring Rule

All Required checks must pass. Any failure = audit FAIL.

## Doctrine Lock

Construction OS v2 Doctrine-Frozen Rollout
