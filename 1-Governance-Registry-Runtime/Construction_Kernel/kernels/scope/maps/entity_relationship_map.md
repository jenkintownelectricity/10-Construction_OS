# Entity Relationship Map — Construction Scope Kernel

## Purpose

This map documents all scope entities and their relationships within the Construction Scope Kernel.

## Entities

| Entity | Primary Key | Description |
|--------|-------------|-------------|
| scope_entry | entry_id | Atomic scope fact (boundary, inclusion, exclusion, trade interface) |
| scope_of_work | scope_id | Aggregated scope package with all subordinate references |
| work_operation | operation_id | Discrete constructible task within a scope |
| sequence_step | step_id | Sequencing record with predecessor/successor relationships |
| trade_responsibility | responsibility_id | Trade assignment within a scope |
| inspection_step | inspection_id | Quality inspection requirement with hold point declarations |
| commissioning_step | step_id | BECx verification step |
| closeout_requirement | requirement_id | Project closeout deliverable |
| warranty_handoff_record | handoff_id | Warranty transfer record |

## Relationships

```
scope_of_work (root)
│
├──► trade_responsibility [1:many via scope_ref]
│      Trade ownership assignments for this scope.
│
├──► work_operation [1:many via scope_ref]
│    │  Constructible tasks within this scope.
│    └──► sequence_step [1:many via scope_ref]
│           Execution ordering with hold points.
│
├──► inspection_step [1:many via scope_ref]
│      Quality hold points and verification requirements.
│
├──► commissioning_step [1:many via scope_ref]
│      BECx verification steps by phase.
│
├──► closeout_requirement [1:many via scope_ref]
│      Project completion deliverables.
│
└──► warranty_handoff_record [1:many via scope_ref]
       Warranty transfer records for closeout.
```

## Shared References (External)

- `interface_zones` — Shared interface zone registry (not owned by this kernel).
- `control_layers_affected` — Shared control layer taxonomy.
- `csi_sections` — CSI MasterFormat section numbers.
- `test_method_ref` — References to ASTM/AAMA test methods (owned by Standards Kernel).

## Referencing Convention

- All relationships use string identifiers (e.g., "SOW-ROOF-001").
- No entity embeds another entity as a nested object.
- Cross-entity references are validated by contract, not by schema enforcement.

## Cardinality Rules

- Every subordinate entity references exactly one scope_of_work via `scope_ref`.
- A scope_of_work may have zero or many of any subordinate entity.
- scope_entry records are independent atomic facts; they may or may not be referenced by a scope_of_work.
