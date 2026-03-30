# Object Model Overview

## Core Object Graph

The Scope Kernel object model is organized around the Scope of Work as the root object. All other objects reference a scope through `scope_ref`.

```
Scope of Work
  |-- Work Operation (1:many)
  |-- Sequence Step (1:many)
  |-- Trade Responsibility (1:many)
  |-- Inspection Step (1:many)
  |-- Commissioning Step (1:many)
  |-- Closeout Requirement (1:many)
  |     |-- Warranty Handoff Record (1:many)
  |-- Interface Zone references (many:many)
  |-- Scope Entry (1:many, atomic facts)
```

## Object Relationships

### Scope of Work to Operations
A scope of work contains one or more work operations. Each operation has a type, trade reference, and optional sequence position.

### Operations to Sequence Steps
Sequence steps order operations across trades. Steps have predecessor/successor relationships forming a directed acyclic graph (DAG).

### Scope to Trade Responsibilities
Each scope maps to one or more trade responsibilities. A trade responsibility defines what a specific trade includes and excludes within that scope.

### Scope to Inspections
Inspection steps define verification checkpoints. They may carry hold points that block successor operations.

### Scope to Commissioning
Commissioning steps align to BECx phases. They reference acceptance criteria and required documentation.

### Scope to Closeout
Closeout requirements define warranty submissions, as-built documentation, and other handoff deliverables.

## Status Lifecycle

All objects follow the same status enum: `active`, `draft`, `deprecated`.

- `draft` -- record is being developed, not yet authoritative
- `active` -- record is the current source of truth
- `deprecated` -- record has been superseded, retained for lineage

## Identity Convention

Each object carries a unique identifier field (e.g., `scope_id`, `operation_id`, `step_id`). Identifiers are opaque strings assigned at creation and never reused.
