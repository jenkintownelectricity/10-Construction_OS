# 200-engines — Boundary

| Property | Value |
|----------|-------|
| Layer | 200-engines |
| Purpose | Deterministic logic consuming truth and graph |
| Write Access | Engine layer commits |
| Read Access | 300, 400 |
| Dependency | Reads from 000, 100 |

## Prohibitions

- MUST NOT write to 000-governance-truth
- MUST NOT write to 100-knowledge-graph
