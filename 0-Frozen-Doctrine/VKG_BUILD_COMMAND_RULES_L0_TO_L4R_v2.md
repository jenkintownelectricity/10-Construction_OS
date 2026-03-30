# Construction OS v2 — VKG Build Command Rules L0 to L4R

## Authority

Armand Lefebvre, L0 — Lefebvre Design Solutions LLC

## Purpose

Defines the rules for issuing build commands within Construction OS v2
under ValidKernel Governance.

## Command Levels

| Level | Role | Authorization |
|-------|------|---------------|
| L0 | Governance Authority | Full system authority |
| L1 | Domain Authority | Domain-scoped authority under L0 |
| L2 | Execution Authority | Task-scoped authority under L1 |
| L3 | Worker Authority | Worker-scoped authority under L2 |
| L4R | Review Authority | Review and verification authority |

## Build Command Rules

1. Every build action requires a governance command
2. Commands must specify the minimum sufficient authority level
3. Higher authority may issue commands at lower levels
4. Lower authority may not issue commands at higher levels
5. All commands produce receipts
6. All commands are registered in the command registry
7. Commands that fail validation must not execute

## Wave-Specific Rules

- Wave 0: L0 only (doctrine genesis)
- Wave 1-2: L0 required (absorption)
- Wave 3+: L0 or L1 with L0 pre-authorization
- All waves: FAIL_CLOSED enforcement

## Doctrine Lock

Construction OS v2 Doctrine-Frozen Rollout
