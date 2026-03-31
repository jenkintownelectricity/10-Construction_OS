# 400-adapters — Boundary

| Property | Value |
|----------|-------|
| Layer | 400-adapters |
| Purpose | Bridges to external systems |
| Write Access | Adapter layer commits |
| Read Access | None (terminal layer) |
| Dependency | Consumes 200, 300 |

## Prohibitions

- MUST NOT modify 000-governance-truth
- MUST NOT build CAD/Revit/AutoCAD plugins (prohibited this wave)
