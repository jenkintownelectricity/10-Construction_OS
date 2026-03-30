# Kernel Scope — Construction Material Kernel

## Domain Boundary

The Construction Material Kernel operates within the material-domain truth surface of CSI Division 07 — Building Envelope Systems. Its scope encompasses the characterization of materials by their physical properties, tested performance, compatibility relationships, weathering behavior, and hygrothermal properties.

## In-Scope Entities

| Entity | Description |
|---|---|
| Material Class | Taxonomy classification (thermoplastic, elastomer, bituminous, etc.) |
| Material Form | Physical delivery form (sheet, liquid, foam, rigid board, etc.) |
| Material Property | Measured physical property with value, unit, and test method |
| Material Performance | Tested performance record under stated conditions |
| Compatibility Record | Material-to-material compatibility assessment |
| Weathering Behavior | Degradation response to environmental exposure |
| Hygrothermal Property | Moisture transport and thermal-moisture interaction properties |
| Standards Reference | ASTM test method citation for property definition |
| Evidence Linkage | Traceable pointer to test reports, TDS, field data |

## Scope Constraints

- Materials are characterized generically by class and properties, never by brand
- All property values require test method references and evidence pointers
- Compatibility results require evidence; untested pairs are flagged as `untested`
- Weathering records are bounded by published test duration
- Hygrothermal properties are valid only at stated temperature and humidity conditions

## Division 07 Focus Areas

| Subdivision | Material Domain |
|---|---|
| 07 10 00 | Dampproofing and waterproofing materials |
| 07 20 00 | Thermal insulation materials |
| 07 30 00 | Steep-slope roofing materials |
| 07 40 00 | Roofing and siding panels |
| 07 50 00 | Membrane roofing materials |
| 07 60 00 | Flashing and sheet metal materials |
| 07 70 00 | Roof and wall specialties materials |
| 07 80 00 | Fire and smoke protection materials |
| 07 90 00 | Joint protection materials |

## Out of Scope

- Specification requirements and obligation language
- Assembly layer sequences and attachment methods
- Chemical reaction mechanisms and cure kinetics
- Project scope boundaries and trade responsibilities
- Cross-kernel intelligence correlation and risk scoring
