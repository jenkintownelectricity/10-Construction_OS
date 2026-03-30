# Trade Responsibility Contract

## Purpose

This contract defines the rules governing trade_responsibility records in the Construction Scope Kernel.

## Identity

- Every trade_responsibility record MUST have a unique `responsibility_id`.
- The `schema_version` MUST be "v1".

## Trade Assignment

- The `trade` field MUST be one of the enumerated trades in the schema.
- Each trade_responsibility record MUST reference exactly one scope_of_work via `scope_ref`.
- A single scope_of_work MAY have multiple trade_responsibility records.

## Boundary Rules

- `inclusions` define the specific work items assigned to this trade.
- `exclusions` define work items explicitly not assigned to this trade.
- Gaps between trade responsibilities within a scope MUST be identified and resolved.
- Overlaps between trade responsibilities MUST be flagged as coordination risks.

## Interface Coordination

- `interface_zones` MUST reference valid interface zone identifiers from the shared registry.
- Where two trades share an interface zone, both MUST have matching interface_zone entries.
- `coordination_notes` SHOULD document sequencing and handoff expectations.

## Immutability

- Active records MUST NOT be modified without creating a new version.
- Deprecated records MUST be retained for audit trail purposes.
- No runtime behavior or execution logic is embedded in trade responsibility records.
