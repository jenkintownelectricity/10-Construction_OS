# Standards-to-Object Map — Construction Scope Kernel

## Purpose

This map documents how industry standards (IBC, CSI MasterFormat) map to scope objects in the Construction Scope Kernel.

## CSI MasterFormat Mapping

Scope objects reference CSI MasterFormat sections via the `csi_sections` array. The following divisions are most relevant to the scope kernel:

| CSI Division | Section Range | Scope Object Coverage |
|-------------|---------------|----------------------|
| Division 04 | 04 00 00 | Masonry scope (trade_responsibility, work_operation) |
| Division 05 | 05 00 00 | Steel scope (trade_responsibility) |
| Division 07 | 07 00 00 | Thermal and moisture protection (primary scope domain) |
| Division 07 | 07 10 00 | Dampproofing and waterproofing |
| Division 07 | 07 20 00 | Thermal insulation |
| Division 07 | 07 27 00 | Air barriers |
| Division 07 | 07 50 00 | Membrane roofing |
| Division 07 | 07 60 00 | Flashing and sheet metal |
| Division 07 | 07 70 00 | Roof and wall specialties |
| Division 07 | 07 90 00 | Joint protection (sealants) |
| Division 08 | 08 00 00 | Glazing scope (trade_responsibility) |

## IBC Code Mapping

Scope objects relate to IBC requirements through inspection and commissioning steps:

| IBC Chapter | Relevance | Scope Entity |
|-------------|-----------|--------------|
| Chapter 15 | Roof assemblies | scope_of_work, inspection_step |
| Chapter 14 | Exterior walls | scope_of_work, inspection_step |
| Chapter 17 | Special inspections | inspection_step (hold_point: true) |
| Chapter 19 | Concrete | trade_responsibility |
| Chapter 26 | Plastic (air/vapor barriers) | trade_responsibility, inspection_step |

## ASTM/AAMA Test Method Mapping

Inspection steps reference test methods via `test_method_ref`:

| Standard | Description | Inspection Type |
|----------|-------------|----------------|
| ASTM E2357 | Air barrier continuity | air_test |
| ASTM D4263 | Substrate moisture | substrate |
| ASTM C1193 | Sealant joint design | visual |
| AAMA 501.2 | Water penetration | flood_test |
| ASTM E1105 | Field water penetration | flood_test |

## Mapping Rules

- CSI sections are stored as strings (e.g., "07 52 00") in scope_of_work.csi_sections.
- IBC references are documented in scope contracts and notes, not in schema fields.
- ASTM/AAMA references are stored in inspection_step.test_method_ref.
- Standards references are informational; the Standards Kernel owns the full standard text.
