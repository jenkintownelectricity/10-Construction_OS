# Inspection Step Contract

## Purpose

This contract defines the rules governing inspection_step records in the Construction Scope Kernel.

## Identity

- Every inspection_step record MUST have a unique `inspection_id`.
- The `schema_version` MUST be "v1".

## Classification

- The `inspection_type` MUST be one of the enumerated types in the schema.
- Each inspection_step MUST reference exactly one scope_of_work via `scope_ref`.

## Hold Points

- When `hold_point` is true, subsequent work operations MUST NOT proceed until the inspection passes.
- Hold points are truth declarations, not runtime controls.

## Acceptance Criteria

- `acceptance_criteria` SHOULD be specific and measurable.
- `test_method_ref` SHOULD reference an industry standard test method (e.g., ASTM, AAMA).

## Evidence

- When `evidence_required` is true, photographic or documented evidence MUST be captured.
- Evidence records link to this inspection via the evidence linkage model.

## Timing

- `timing` defines when the inspection occurs relative to work operations.
- Pre-cover inspections MUST occur before concealment of the inspected assembly.

## Immutability

- Active records MUST NOT be modified without creating a new version.
- Deprecated records MUST be retained for audit trail purposes.
- No runtime behavior or execution logic is embedded in inspection records.
