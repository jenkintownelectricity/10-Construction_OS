# Material Compatibility Contract

## Contract ID
CONTRACT-MATL-COMPAT-001

## Purpose
Defines the interface contract for external consumers querying material compatibility records from the Construction Material Kernel.

## Provider
Construction Material Kernel (KERN-CONST-MATL)

## Consumers
- Construction_Assembly_Kernel — compatibility checks for assembly layer adjacency
- Construction_Chemistry_Kernel — compatibility data for chemistry analysis
- Construction_Reference_Intelligence — compatibility matrices for risk analysis

## Schema Reference
`schemas/material_compatibility_record.schema.json`

## Guaranteed Fields
| Field | Type | Always Present |
|---|---|---|
| schema_version | string | Yes |
| record_id | string | Yes |
| material_a_ref | string | Yes |
| material_b_ref | string | Yes |
| compatibility_result | enum | Yes |
| status | enum | Yes |

## Result Enum Contract
`compatibility_result` values are frozen: compatible, incompatible, conditional, untested. Consumers must handle all four values.

## Consumer Obligations
- `compatible` — no material interaction restrictions
- `incompatible` — consumers must enforce physical separation
- `conditional` — consumers must read and enforce the `conditions` field
- `untested` — consumers must treat as unknown risk; must not assume compatibility

## Stability Guarantee
This contract is frozen at baseline `construction-kernel-pass-2`. Compatibility results may be revised through the revision lineage model, but the contract structure is stable.

## Fail-Closed Behavior
If no compatibility record exists for a material pair, consumers must treat the pair as `untested`. Absence of a record never implies compatibility.
