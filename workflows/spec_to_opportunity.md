# Workflow: Spec to Opportunity

## Application
Spec Intelligence App

## Trigger
User submits raw specification document text.

## Pipeline Stages

| Stage | Component | Fail Behavior |
|-------|-----------|---------------|
| 1. Normalize | Spec parser normalizer | Halt on normalization failure |
| 2. Parse | Spec parser | Halt on empty/invalid input |
| 3. Structural Validate | Structural validator | Halt on missing fields |
| 4. Domain Validate | Domain validator | Halt on requirement rule violations |
| 5. Adapt | Spec adapter | Halt on translation failure |
| 6. Spec Engine | Spec engine | Halt on analysis failure |
| 7. Contract Validate | Schema validation | Halt on output contract violation |
| 8. Package | Deliverable model | Package intelligence output |
| 9. Audit | Audit logger | Log all events |

## Output
Intelligence report with opportunities, requirement summaries, and reference analysis.
