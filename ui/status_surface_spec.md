# Status Surface Spec — Construction Application OS v0.1

## Status
Conceptual only. No UI implementation in this pass.

## Status Surfaces (Conceptual)

| Surface | Description |
|---------|-------------|
| Pipeline Status | Current stage of active workflow (e.g., "Validating", "Generating geometry") |
| Validation Status | Pass/fail status for each validation stage |
| Deliverable Status | Generated/failed/skipped for each output format |
| Audit Summary | Count of events, warnings, errors for current run |

## Data Source
All status data derives from Construction_Runtime pipeline execution. The application layer reads status; it does not compute it.
