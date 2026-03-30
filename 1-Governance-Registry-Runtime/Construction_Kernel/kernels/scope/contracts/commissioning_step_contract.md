# Commissioning Step Contract

## Purpose

This contract defines the rules governing commissioning_step records in the Construction Scope Kernel.

## Identity

- Every commissioning_step record MUST have a unique `step_id`.
- The `schema_version` MUST be "v1".

## BECx Phase

- The `becx_phase` MUST be one of the enumerated phases in the schema.
- Each commissioning_step MUST reference exactly one scope_of_work via `scope_ref`.
- Commissioning steps follow the building enclosure commissioning (BECx) process.

## Acceptance Criteria

- `acceptance_criteria` SHOULD be specific and measurable.
- Performance testing steps MUST define pass/fail thresholds.

## Documentation

- `documentation_required` lists all documents that must be produced or collected.
- Documentation requirements are truth declarations tied to the scope record.
- The commissioning authority is identified via `responsible_party`.

## Sequencing

- Design review steps precede construction observation steps.
- Pre-cover inspections precede performance testing.
- Closeout review follows all field activities.
- Seasonal observation may extend beyond project closeout.

## Immutability

- Active records MUST NOT be modified without creating a new version.
- Deprecated records MUST be retained for audit trail purposes.
- No runtime behavior or execution logic is embedded in commissioning records.
