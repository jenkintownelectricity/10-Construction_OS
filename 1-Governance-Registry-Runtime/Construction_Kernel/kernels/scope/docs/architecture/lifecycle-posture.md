# Lifecycle Posture

## Purpose

Defines how the Scope Kernel's truth spans the full project lifecycle from design through closeout. Scope is not static -- it evolves through project phases.

## Lifecycle Phases

### 1. Design Phase
- Scope is defined at a conceptual level.
- Trade responsibilities may be preliminary.
- Scope records carry `status: draft`.
- Interface zones are identified but may not have full trade assignments.

### 2. Procurement Phase
- Scope is refined to align with bid packages.
- Trade responsibilities become contractual.
- Inclusions and exclusions are formalized.
- Scope records may transition from `draft` to `active`.

### 3. Construction Phase
- Scope is executed. Work operations are performed per sequencing.
- Inspection steps are triggered at hold points.
- Scope gaps discovered during construction are flagged immediately.
- Commissioning observations begin (construction_observation phase).

### 4. Commissioning Phase
- BECx steps are executed: pre-cover inspections, performance testing.
- Scope verification occurs against acceptance criteria.
- Deficiencies generate scope-related punch list items.

### 5. Closeout Phase
- Warranty submissions are collected per closeout requirements.
- As-built documentation is assembled.
- Maintenance manuals and training are delivered.
- Warranty handoff records are finalized.

## Scope Record Lifecycle

```
draft --> active --> deprecated
  |                     ^
  |                     |
  +--- (revision) ------+
```

- Records are never deleted. Deprecated records are retained for revision lineage.
- Each transition is tracked in the revision lineage model.

## Phase-to-Object Mapping

| Lifecycle Phase | Primary Scope Objects |
|---|---|
| Design | Scope of Work, Trade Responsibility |
| Procurement | Scope of Work, Trade Responsibility, Closeout Requirements |
| Construction | Work Operations, Sequence Steps, Inspection Steps |
| Commissioning | Commissioning Steps, Inspection Steps |
| Closeout | Closeout Requirements, Warranty Handoff Records |

## Seasonal Considerations

Some scope activities are phase-constrained by season. The kernel records these constraints through `weather_constraints` fields on operations and sequence steps without making scheduling decisions.
