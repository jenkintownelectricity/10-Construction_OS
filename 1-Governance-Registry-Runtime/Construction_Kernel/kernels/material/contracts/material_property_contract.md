# Material Property Contract

## Contract ID
CONTRACT-MATL-PROP-001

## Purpose
Defines the interface contract for external consumers querying material property records from the Construction Material Kernel.

## Provider
Construction Material Kernel (KERN-CONST-MATL)

## Consumers
- Construction_Specification_Kernel — property values for spec compliance checks
- Construction_Assembly_Kernel — property values for assembly compatibility
- Construction_Reference_Intelligence — property values for cross-kernel analysis

## Schema Reference
`schemas/material_property.schema.json`

## Guaranteed Fields
| Field | Type | Always Present |
|---|---|---|
| schema_version | string | Yes |
| property_id | string | Yes |
| material_ref | string | Yes |
| property_name | string | Yes |
| value | number or string | Yes |
| unit | string | Yes |
| test_method_ref | string | Yes |
| status | enum | Yes |

## Value Interpretation Rules
- Numeric values are in the stated unit; consumers must not convert without explicit unit mapping
- String values represent pass/fail or classification results
- Values are valid only under stated conditions (see optional `conditions` field)
- Values without a `temperature_range` field are assumed tested at standard conditions (73 deg F, 50% RH)

## Stability Guarantee
This contract is frozen at baseline `construction-kernel-pass-2`. Required fields will not change. Optional fields may be added. Property values may be revised through the revision lineage model.

## Fail-Closed Behavior
If a queried property does not exist for a material, consumers must not assume a default value. Missing properties indicate data gaps, not zero or null values.
