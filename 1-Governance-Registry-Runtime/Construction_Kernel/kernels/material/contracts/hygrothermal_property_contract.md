# Hygrothermal Property Contract

## Contract ID
CONTRACT-MATL-HYGRO-001

## Purpose
Defines the interface contract for external consumers querying hygrothermal property records from the Construction Material Kernel.

## Provider
Construction Material Kernel (KERN-CONST-MATL)

## Consumers
- Construction_Assembly_Kernel — hygrothermal data for moisture management analysis
- Construction_Reference_Intelligence — hygrothermal properties for risk modeling

## Schema Reference
`schemas/hygrothermal_property.schema.json`

## Guaranteed Fields
| Field | Type | Always Present |
|---|---|---|
| schema_version | string | Yes |
| property_id | string | Yes |
| material_ref | string | Yes |
| property_type | enum | Yes |
| value | number or string | Yes |
| unit | string | Yes |
| status | enum | Yes |

## Property Type Enum Contract
`property_type` values are frozen: vapor_permeance, moisture_absorption, capillary_coefficient, sorption_isotherm, thermal_conductivity_wet. New values may be appended; existing values are never removed.

## Consumer Obligations
- Hygrothermal values are valid only at stated temperature and RH conditions
- Consumers must check `temperature` and `rh_conditions` fields before applying values
- Wet-cup and dry-cup permeance are distinct records with different test conditions
- Consumers must not use hygrothermal data for simulation without verifying condition alignment

## Stability Guarantee
This contract is frozen at baseline `construction-kernel-pass-2`. Required fields and enum values will not change within this baseline.

## Fail-Closed Behavior
If no hygrothermal property exists for a material and property type, consumers must not assume a default value. Missing hygrothermal data indicates a data gap.
