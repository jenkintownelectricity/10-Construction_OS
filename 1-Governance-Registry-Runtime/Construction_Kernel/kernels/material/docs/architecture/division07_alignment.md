# Division 07 Alignment — Construction Material Kernel

## CSI MasterFormat Division 07 — Thermal and Moisture Protection

This kernel's initial domain focus is CSI Division 07, which covers building envelope materials for thermal control, moisture management, air barriers, vapor retarders, roofing, waterproofing, fireproofing, and joint sealants.

## Division 07 Subdivisions and Material Kernel Coverage

| Number | Title | Material Classes Covered |
|---|---|---|
| 07 10 00 | Dampproofing and Waterproofing | bituminous, fluid_applied, sheet_applied |
| 07 20 00 | Thermal Insulation | cellular_plastic, mineral_fiber, composite |
| 07 21 00 | Thermal Insulation — Board | cellular_plastic (polyiso, XPS, EPS) |
| 07 22 00 | Thermal Insulation — Blanket | mineral_fiber (fiberglass, mineral wool) |
| 07 27 00 | Thermal Insulation — Sprayed | spray_applied (SPF) |
| 07 30 00 | Steep Slope Roofing | composite, metallic, cementitious |
| 07 40 00 | Roofing and Siding Panels | metallic, composite |
| 07 50 00 | Membrane Roofing | thermoplastic, thermoset, elastomer, bituminous |
| 07 52 00 | Modified Bitumen Membrane | bituminous |
| 07 54 00 | Thermoplastic Membrane | thermoplastic (TPO, PVC) |
| 07 55 00 | EPDM Membrane | thermoset |
| 07 60 00 | Flashing and Sheet Metal | metallic, elastomer, sheet_applied |
| 07 70 00 | Roof Specialties | metallic, composite |
| 07 80 00 | Fire and Smoke Protection | mineral_fiber, cementitious |
| 07 90 00 | Joint Protection | elastomer, fluid_applied |
| 07 92 00 | Joint Sealants | elastomer, fluid_applied |

## Control Layer Mappings

Materials in this kernel map to building envelope control layers:

| Control Layer | Relevant Material Classes |
|---|---|
| Water control | bituminous, thermoplastic, thermoset, fluid_applied, sheet_applied |
| Air control | fluid_applied, sheet_applied, thermoplastic |
| Vapor control | sheet_applied, fluid_applied, thermoplastic |
| Thermal control | cellular_plastic, mineral_fiber, spray_applied |
| Fire control | mineral_fiber, cementitious |

## Alignment Constraints

- Material records must reference applicable Division 07 subdivisions
- Control layer mappings use the shared control_layers.json registry
- Material classes must use the shared taxonomy enum values
- This kernel covers material truth only — assembly configurations for Division 07 systems belong to the Assembly Kernel
