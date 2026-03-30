# Kernel Map — Construction Scope Kernel

## Purpose

This map provides an overview of the Construction Scope Kernel and the relationships between its primary entities.

## Core Entity

The **scope_of_work** is the root entity. It defines the boundary of a scope package and references all subordinate entities.

## Entity Relationships

```
scope_of_work
├── trade_responsibility (1:many)
├── work_operation (1:many)
│   └── sequence_step (1:many)
├── inspection_step (1:many)
├── commissioning_step (1:many)
├── closeout_requirement (1:many)
└── warranty_handoff_record (1:many)
```

## Reference Linkages

- `scope_entry` records capture atomic scope facts (boundaries, inclusions, exclusions).
- `scope_of_work` records aggregate scope entries into constructible packages.
- `trade_responsibility` records assign ownership within a scope.
- `work_operation` and `sequence_step` records define execution order.
- `inspection_step` records define quality hold points.
- `commissioning_step` records define BECx verification points.
- `closeout_requirement` and `warranty_handoff_record` records define project completion deliverables.

## Shared References

- `interface_zones` — from the shared interface zone registry.
- `control_layers_affected` — from the shared control layer taxonomy.
- `csi_sections` — CSI MasterFormat section numbers.

## Principles

- All entities are truth records, not runtime objects.
- All references use string identifiers, not embedded objects.
- No entity contains execution logic or behavioral code.
- The kernel is read-only at runtime; mutations occur through versioned updates.
