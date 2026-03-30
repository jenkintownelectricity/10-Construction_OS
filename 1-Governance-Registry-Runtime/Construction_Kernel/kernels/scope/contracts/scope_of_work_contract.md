# Scope of Work Contract

## Purpose

This contract defines the rules governing scope_of_work records in the Construction Scope Kernel.

## Identity

- Every scope_of_work record MUST have a unique `scope_id`.
- The `schema_version` MUST be "v1".
- The `title` MUST be a human-readable description of the scope package.

## Classification

- The `scope_type` MUST be one of: division_scope, trade_scope, interface_scope, phased_scope.
- The `status` MUST be one of: active, draft, deprecated.

## Boundary Rules

- `inclusions` define what is explicitly inside the scope boundary.
- `exclusions` define what is explicitly outside the scope boundary.
- Every item that could be ambiguous MUST appear in either inclusions or exclusions.
- Inclusions and exclusions MUST NOT overlap.

## References

- `trade_responsibilities` MUST reference valid trade_responsibility records.
- `operations` MUST reference valid work_operation records.
- `inspection_steps` MUST reference valid inspection_step records.
- `commissioning_steps` MUST reference valid commissioning_step records.
- `closeout_requirements` MUST reference valid closeout_requirement records.

## Immutability

- Active scope records MUST NOT be modified without creating a new version.
- Deprecated records MUST be retained for audit trail purposes.
- No runtime behavior or execution logic is embedded in scope records.
