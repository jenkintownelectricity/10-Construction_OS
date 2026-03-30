# Construction OS v2 — Governance Package

## Authority

Armand Lefebvre, L0 — Lefebvre Design Solutions LLC

## Governance Model

Construction OS v2 operates under ValidKernel Governance (VKG) v0.1.
All actions within this domain must follow the VKG command protocol.

## Command Protocol

Every governed action follows the canonical governance loop:

```
Authority → Command → Runtime Gate → Execution → Receipt → Registry → Verification
```

## Ring Structure

All commands must include four rings:

- **L0 — Governance Context:** Authority, ID, date, risk class, scope
- **L1 — Mission Directive:** Objective, outcomes, constraints, non-goals
- **L2 — Deterministic Commit Gate:** Validation checklist with gate rule
- **L3 — Capability Bound:** TOUCH-ALLOWED, NO-TOUCH, enforcement mode

## Enforcement

- **Mode:** FAIL_CLOSED
- If validation fails or state is uncertain, execution must not proceed
- No action may bypass the governance gate
- No implicit permissions exist

## Risk Classes

| Class | Description |
|-------|-------------|
| RC1 | Low-risk: documentation updates |
| RC2 | Moderate-risk: governance or spec changes |
| RC3 | High-risk: architecture or security changes |
| RC4 | Critical: requires explicit L0 authorization |

## Doctrine Lock

Construction OS v2 Doctrine-Frozen Rollout
