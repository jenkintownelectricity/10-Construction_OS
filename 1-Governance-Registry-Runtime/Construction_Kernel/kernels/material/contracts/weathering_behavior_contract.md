# Weathering Behavior Contract

## Contract ID
CONTRACT-MATL-WTHR-001

## Purpose
Defines the interface contract for external consumers querying weathering behavior records from the Construction Material Kernel.

## Provider
Construction Material Kernel (KERN-CONST-MATL)

## Consumers
- Construction_Assembly_Kernel — weathering data for assembly durability assessment
- Construction_Reference_Intelligence — weathering patterns for risk correlation

## Schema Reference
`schemas/weathering_behavior.schema.json`

## Guaranteed Fields
| Field | Type | Always Present |
|---|---|---|
| schema_version | string | Yes |
| behavior_id | string | Yes |
| material_ref | string | Yes |
| exposure_type | enum | Yes |
| degradation_rate | string | Yes |
| status | enum | Yes |

## Exposure Type Enum Contract
`exposure_type` values are frozen: uv, thermal_cycling, moisture, freeze_thaw, chemical, biological. New values may be appended; existing values are never removed.

## Consumer Obligations
- Degradation rates are bounded by the test duration stated in the record
- Consumers must not extrapolate degradation rates beyond the tested duration
- Climate context, when present, limits the applicability of the weathering data
- Service life impact values are published claims, not kernel-generated predictions

## Stability Guarantee
This contract is frozen at baseline `construction-kernel-pass-2`. Required fields and enum values will not change within this baseline.

## Fail-Closed Behavior
If no weathering record exists for a material and exposure type, consumers must not assume weathering resistance. Absence of weathering data indicates a data gap.
