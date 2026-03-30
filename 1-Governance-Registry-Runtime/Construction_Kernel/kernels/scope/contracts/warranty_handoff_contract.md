# Warranty Handoff Contract

## Purpose

This contract defines the rules governing warranty_handoff_record entries in the Construction Scope Kernel.

## Identity

- Every warranty_handoff_record MUST have a unique `handoff_id`.
- The `schema_version` MUST be "v1".

## Classification

- The `warranty_type` MUST be one of: manufacturer_standard, manufacturer_extended, system_warranty, nol, workmanship.
- Each warranty_handoff_record MUST reference exactly one scope_of_work via `scope_ref`.

## Duration and Trigger

- `duration_years` defines the warranty coverage period in years.
- `start_trigger` defines the event that initiates warranty coverage.
- NDL (No Dollar Limit) warranties typically require manufacturer inspection before issuance.

## Conditions and Exclusions

- `conditions` define requirements that must be met for warranty validity.
- `exclusions` define situations not covered by the warranty.
- Conditions typically include approved installer requirements and maintenance obligations.

## Documentation

- `documentation_required` lists all documents needed to activate the warranty.
- Common requirements include: installer certification, inspection reports, product submittals, maintenance agreements.
- Missing documentation MAY void warranty coverage.

## Immutability

- Active records MUST NOT be modified without creating a new version.
- Deprecated records MUST be retained for audit trail purposes.
- No runtime behavior or execution logic is embedded in warranty records.
