# Kernel-to-Inspection Map — Construction Scope Kernel

## Purpose

This map defines how the scope kernel establishes inspection hold points and quality verification requirements within scope boundaries.

## Scope-Defined Inspection Points

The scope kernel declares inspection requirements as truth records. Each `inspection_step` record is owned by a `scope_of_work` and defines:

- **What** is inspected (inspection_type: pre_cover, substrate, adhesion, continuity, etc.)
- **When** inspection occurs (timing relative to work operations)
- **Who** inspects (responsible_party)
- **What passes** (acceptance_criteria, test_method_ref)
- **Whether work stops** (hold_point: true/false)

## Hold Point Logic

- When `hold_point` is true, the scope declares that no subsequent work operation may proceed until the inspection passes.
- Hold points are declarative truth, not runtime enforcement.
- A runtime or worker system reads hold points and enforces sequencing.

## Relationship to Work Operations

```
scope_of_work
├── work_operation (sequence_position: 1) — Surface prep
├── inspection_step (hold_point: true) — Substrate inspection
├── work_operation (sequence_position: 2) — Installation
├── inspection_step (hold_point: true) — Pre-cover inspection
└── work_operation (sequence_position: 3) — Protection
```

## Evidence Linkage

- When `evidence_required` is true, the scope declares that documented evidence must be captured.
- Evidence records (photos, reports) link back to the inspection_step via its `inspection_id`.
- The scope kernel does not store evidence; it declares the requirement.

## Commissioning Overlap

- BECx commissioning steps may reference the same assemblies as inspection steps.
- Commissioning steps verify system-level performance; inspection steps verify component-level quality.
- Both are owned by the scope_of_work but serve different verification purposes.

## Principles

- The scope kernel declares what must be inspected. It does not perform inspections.
- Inspection records are immutable truth. Results are stored outside the kernel.
- All inspection requirements are traceable to a specific scope_of_work record.
