# Construction OS v2 — Branch Protection Policy

## Authority

Armand Lefebvre, L0 — Lefebvre Design Solutions LLC

## Generated

2026-03-30 — Wave 0 Genesis

## Policy

### main branch

- **Direct push:** Prohibited
- **Required reviews:** 1 (L0 authority)
- **Status checks:** Required (when CI is configured)
- **Force push:** Prohibited
- **Deletion:** Prohibited

### Feature branches

- Must follow naming convention: `claude/<descriptor>` or `feature/<descriptor>`
- Must be created from `main`
- Must be merged via pull request
- Must not be force-pushed after review begins

### Governance branches

- Branches prefixed with `claude/construction-os-v2-` are governance branches
- Governance branches require L0 review before merge to main
- Governance branches must reference the authorizing command ID

## Doctrine Lock

Construction OS v2 Doctrine-Frozen Rollout
