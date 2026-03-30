# Transition Condition Contract

## Purpose

Defines the truth exchange contract for transition_condition records. Transitions document how two assembly systems connect at interface zones.

## Schema

`schemas/transition_condition.schema.json`

## Required Fields

| Field | Type | Constraint |
|---|---|---|
| schema_version | string | Must be "v1" |
| transition_id | string | Unique, non-empty |
| title | string | Human-readable description |
| interface_zone | enum | Must be one of 10 interface zone IDs from shared registry |
| from_assembly_ref | string | Valid assembly_system ID |
| to_assembly_ref | string | Valid assembly_system ID |
| status | enum | active, draft, deprecated |

## Invariants

1. Every transition must reference two valid assembly systems.
2. The interface_zone must be from the shared interface zone registry.
3. If risk_level is critical or high, evidence_refs should be populated.
4. Control layers listed in control_layers_maintained must be valid control layer IDs.
5. from_assembly_ref and to_assembly_ref must be different systems.

## Risk Posture

Transitions are high-risk objects. All transitions at roof_to_wall and parapet_transition interface zones default to critical risk unless evidence supports a lower assessment.

## Consumers

- Construction_Reference_Intelligence — interface risk analysis
- Continuity verification tools — check that required control layers are maintained

## Change Policy

Transition records follow append-only revision. Deprecated transitions retain their evidence references.
