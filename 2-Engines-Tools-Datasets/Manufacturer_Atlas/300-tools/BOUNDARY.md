# 300-tools — Boundary

| Property | Value |
|----------|-------|
| Layer | 300-tools |
| Purpose | Operator-facing tools and UI surfaces |
| Write Access | Tool layer commits |
| Read Access | 400 |
| Dependency | Calls 200-engines only |

## Prohibitions

- MUST NOT write to 000-governance-truth
- MUST NOT write to 100-knowledge-graph
- MUST NOT write to 200-engines
