# Workflow: Assembly to Shop Drawing

## Application
Assembly Parser App

## Trigger
User submits raw manufacturer assembly letter text.

## Pipeline Stages

| Stage | Component | Fail Behavior |
|-------|-----------|---------------|
| 1. Normalize | Assembly parser normalizer | Halt on normalization failure |
| 2. Parse | Assembly parser | Halt on empty/invalid input |
| 3. Structural Validate | Structural validator | Halt on missing fields, type errors |
| 4. Domain Validate | Domain validator | Halt on material/assembly rule violations |
| 5. Adapt | Assembly adapter | Halt on translation failure |
| 6. Constraint Check | Constraint engine | Halt on unresolved constraints |
| 7. Assembly Engine | Assembly engine | Halt on incomplete build |
| 8. Geometry | Geometry engine | Halt on dimension/layout failure |
| 9. Generation Validate | Generation validator | Halt on geometry incompleteness |
| 10. DXF Output | DXF writer | Halt on write failure |
| 11. SVG Output | SVG writer | Halt on write failure |
| 12. Package | Deliverable model | Package dual-format deliverable |
| 13. Audit | Audit logger | Log all events |

## Output
DeliverableModel with DXF, SVG, and JSON preview formats.
