# 000-governance-truth — Boundary

| Property | Value |
|----------|-------|
| Layer | 000-governance-truth |
| Status | FROZEN v1.0 |
| Purpose | Canonical manufacturer authority |
| Write Access | Governed commits only (thaw/refreeze) |
| Read Access | All layers |

## Contains

- Schemas and type definitions (090-schemas)
- Assembly constraint sets (080-constraint-sets)
- Manufacturer truth categories (010-070)
- Governance state marker (.governance_state)

## Prohibitions

- Engines (200) MUST NOT write here
- Tools (300) MUST NOT write here
- Adapters (400) MUST NOT write here
- Changes require THAW_REFREEZE_PROTOCOL
