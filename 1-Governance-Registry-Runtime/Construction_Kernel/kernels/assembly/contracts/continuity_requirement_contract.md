# Continuity Requirement Contract

## Purpose

Defines the truth exchange contract for continuity_requirement records. Continuity requirements define rules for control-layer continuity across assemblies and boundaries.

## Schema

`schemas/continuity_requirement.schema.json`

## Required Fields

| Field | Type | Constraint |
|---|---|---|
| schema_version | string | Must be "v1" |
| requirement_id | string | Unique, non-empty |
| control_layer_id | enum | Must be one of 11 control layer IDs from shared registry |
| continuity_type | enum | must_be_continuous, may_be_interrupted, must_terminate, must_transition |
| scope | string | Defines where the requirement applies |

## Invariants

1. The control_layer_id must reference the shared control layer registry.
2. The scope must be specific enough to determine where the requirement applies.
3. Conflicting requirements for the same control_layer_id in overlapping scopes must be flagged.
4. Requirements driven by code sections should reference the code in the conditions field.
5. Requirements do not override tested assembly records — a tested configuration that interrupts a control layer is valid if the test proves adequate performance.

## Scope Examples

- "Entire building enclosure" — applies everywhere
- "All roof-to-wall transitions in climate zones 4-8" — conditional scope
- "Fire-rated wall assemblies per IBC Table 602" — code-driven scope
- "Below-grade assemblies below the water table" — condition-specific scope

## Consumers

- Continuity verification tools — compare requirements against actual assembly configurations
- Construction_Reference_Intelligence — identify assemblies that may violate continuity requirements

## Change Policy

Requirements follow revisable_with_audit posture. Changes require documented justification and may trigger review of affected assembly records.
