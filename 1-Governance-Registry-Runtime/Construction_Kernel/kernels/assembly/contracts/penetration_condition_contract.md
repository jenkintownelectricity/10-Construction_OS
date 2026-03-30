# Penetration Condition Contract

## Purpose

Defines the truth exchange contract for penetration_condition records. Penetrations document how elements pass through building enclosure assemblies.

## Schema

`schemas/penetration_condition.schema.json`

## Required Fields

| Field | Type | Constraint |
|---|---|---|
| schema_version | string | Must be "v1" |
| penetration_id | string | Unique, non-empty |
| title | string | Human-readable description |
| penetration_type | enum | pipe, conduit, structural, equipment, anchor, vent |
| assembly_ref | string | Valid assembly_system ID |
| status | enum | active, draft, deprecated |

## Invariants

1. Every penetration must reference a valid assembly system.
2. The penetration_type must be from the schema-defined enum.
3. Control layers listed in control_layers_affected must be valid control layer IDs.
4. If a seal_method is specified, it should describe how control-layer continuity is restored.
5. Penetrations through fire-rated assemblies must note fire_smoke_control in control_layers_affected.

## Risk Posture

Penetrations default to high risk. Structural penetrations and equipment penetrations default to critical. Risk may be reduced with evidence of effective seal method.

## Consumers

- Construction_Reference_Intelligence — penetration failure pattern analysis
- Inspection workflow tools — penetration seal verification checklists

## Change Policy

Penetration records follow append-only revision. New penetrations in existing assemblies create new records; they do not modify the assembly system record.
