# Closeout Requirement Contract

## Purpose

This contract defines the rules governing closeout_requirement records in the Construction Scope Kernel.

## Identity

- Every closeout_requirement record MUST have a unique `requirement_id`.
- The `schema_version` MUST be "v1".

## Classification

- The `closeout_type` MUST be one of the enumerated types in the schema.
- Each closeout_requirement MUST reference exactly one scope_of_work via `scope_ref`.

## Responsibility

- `responsible_party` identifies who must fulfill the closeout deliverable.
- The responsible party is typically the trade contractor or general contractor.

## Timing

- `due_date_relative` defines when the deliverable is due relative to a project milestone.
- Warranty submissions are typically due at or before substantial completion.
- As-built documentation is due before final completion.
- Training and spare materials are due before occupancy.

## Completeness

- Every scope_of_work SHOULD have at minimum: warranty_submission, as_built_documentation, and final_inspection closeout requirements.
- Punch list items MUST be resolved before final inspection approval.

## Immutability

- Active records MUST NOT be modified without creating a new version.
- Deprecated records MUST be retained for audit trail purposes.
- No runtime behavior or execution logic is embedded in closeout records.
