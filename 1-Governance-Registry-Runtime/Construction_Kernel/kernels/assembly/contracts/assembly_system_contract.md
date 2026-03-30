# Assembly System Contract

## Purpose

Defines the truth exchange contract for assembly_system records. Any system reading or writing assembly systems must comply with this contract.

## Schema

`schemas/assembly_system.schema.json`

## Required Fields

| Field | Type | Constraint |
|---|---|---|
| schema_version | string | Must be "v1" |
| system_id | string | Unique, non-empty |
| title | string | Human-readable |
| assembly_type | enum | roof_assembly, wall_assembly, below_grade_assembly, plaza_assembly, vegetated_assembly, hybrid_assembly |
| status | enum | active, draft, deprecated |

## Invariants

1. Every assembly_system must pass JSON Schema validation before entering the kernel.
2. A system_id must be unique across all assembly_system records.
3. Status must be `draft` if any required field is missing or ambiguity is flagged.
4. Only one version of a system_id may have `status: active` at any time.
5. Layers, if present, must be ordered by `position` with no gaps or duplicates.
6. Control layer IDs must reference the shared registry.
7. Material references must be syntactically valid identifiers (resolution is deferred).

## Consumers

- Construction_Reference_Intelligence — reads for pattern analysis
- Construction_Scope_Kernel — references assembly IDs for scope delineation
- Internal transition, penetration, and edge conditions — reference by assembly_ref

## Producers

- Assembly domain experts authoring kernel truth
- Tested assembly configuration imports

## Change Policy

Schema changes require version bump and frozen-seam coordination. Field additions require schema update and consumer notification.
