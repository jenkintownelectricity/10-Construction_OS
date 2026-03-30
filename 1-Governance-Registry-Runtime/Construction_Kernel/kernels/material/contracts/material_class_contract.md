# Material Class Contract

## Contract ID
CONTRACT-MATL-CLASS-001

## Purpose
Defines the interface contract for external consumers querying material class records from the Construction Material Kernel.

## Provider
Construction Material Kernel (KERN-CONST-MATL)

## Consumers
- Construction_Specification_Kernel — material class references in spec requirements
- Construction_Assembly_Kernel — material class for assembly layer definitions
- Construction_Chemistry_Kernel — material class for chemistry analysis context
- Construction_Reference_Intelligence — material class for cross-kernel correlation

## Schema Reference
`schemas/material_class.schema.json`

## Guaranteed Fields
| Field | Type | Always Present |
|---|---|---|
| schema_version | string | Yes |
| class_id | string | Yes |
| name | string | Yes |
| primary_material_class | enum | Yes |
| status | enum | Yes |

## Enum Contract
`primary_material_class` values are frozen: thermoplastic, thermoset, elastomer, bituminous, cementitious, metallic, mineral_fiber, cellular_plastic, composite, fluid_applied, sheet_applied, spray_applied. New values may be appended; existing values are never removed.

## Stability Guarantee
This contract is frozen at baseline `construction-kernel-pass-2`. Required fields and enum values will not change within this baseline. Optional fields may be added.

## Fail-Closed Behavior
If a queried class_id does not exist, the kernel returns no record. Consumers must not infer class properties from absence of data.
