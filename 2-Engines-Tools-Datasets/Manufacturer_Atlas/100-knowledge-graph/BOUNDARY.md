# 100-knowledge-graph — Boundary

| Property | Value |
|----------|-------|
| Layer | 100-knowledge-graph |
| Purpose | Atlas graph and detail graph structures |
| Write Access | Knowledge layer commits |
| Read Access | 200, 300, 400, 900 |
| Dependency | Reads from 000-governance-truth |

## Contains

- Atlas nodes (110)
- Atlas edges (120)
- Atlas lenses (130)
- Detail graph relations (140)
- Resolution patterns (150)
- Coverage models (160)
- Integrity reports (170)

## Rules

- This layer organizes truth but does not redefine it
- All node/edge data must conform to 000-governance-truth schemas
