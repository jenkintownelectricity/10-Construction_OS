# Taxonomy — Construction Specification Kernel

## CSI Division 07 Section Taxonomy

This kernel organizes specification truth using CSI MasterFormat section numbers as the primary classification system. Each section maps to one or more specification families and control functions.

## Taxonomy Structure

The taxonomy has three levels:

1. **Division** — Division 07 (Thermal and Moisture Protection)
2. **Section** — Six-digit CSI MasterFormat number (e.g., 07 52 00)
3. **Specification Family** — Functional grouping of related sections

## Specification Families

### Waterproofing Family
Sections governing below-grade and horizontal waterproofing systems.

- 07 10 00 — Dampproofing and Waterproofing (general)
- 07 11 00 — Dampproofing
- 07 13 00 — Sheet Waterproofing
- 07 14 00 — Fluid-Applied Waterproofing
- 07 16 00 — Cementitious and Reactive Waterproofing

**Control functions:** bulk_water_control, capillary_control

### Insulation Family
Sections governing thermal insulation systems.

- 07 21 00 — Thermal Insulation
- 07 22 00 — Roof and Deck Insulation
- 07 24 00 — Exterior Insulation and Finish Systems (EIFS)

**Control functions:** thermal_control, protection_layer

### Weather Barrier Family
Sections governing air barriers, vapor retarders, and weather-resistive barriers.

- 07 25 00 — Weather Barriers
- 07 26 00 — Vapor Retarders
- 07 27 00 — Air Barriers

**Control functions:** air_control, vapor_control, bulk_water_control

### Membrane Roofing Family
Sections governing low-slope membrane roofing systems.

- 07 51 00 — Built-Up Bituminous Roofing
- 07 52 00 — Modified Bituminous Membrane Roofing
- 07 53 00 — Elastomeric Membrane Roofing (EPDM)
- 07 54 00 — Thermoplastic Membrane Roofing (TPO, PVC)
- 07 55 00 — Protected Membrane Roofing (IRMA)
- 07 56 00 — Fluid-Applied Roofing

**Control functions:** bulk_water_control, weathering_surface

### Steep-Slope Roofing Family
Sections governing steep-slope roofing systems.

- 07 31 00 — Shingles and Shakes
- 07 32 00 — Roof Tiles
- 07 41 00 — Roof Panels

**Control functions:** weathering_surface, bulk_water_control

### Flashing Family
Sections governing flashing and sheet metal work.

- 07 60 00 — Flashing and Sheet Metal
- 07 62 00 — Sheet Metal Flashing and Trim
- 07 65 00 — Flexible Flashing

**Control functions:** bulk_water_control, drainage_plane

### Fire Protection Family
Sections governing firestopping and smoke seals.

- 07 84 00 — Firestopping
- 07 86 00 — Smoke Seals

**Control functions:** fire_smoke_control

### Sealant Family
Sections governing joint sealants and expansion joints.

- 07 92 00 — Joint Sealants
- 07 95 00 — Expansion Joint Cover Assemblies

**Control functions:** air_control, bulk_water_control, movement_control

## Shared Taxonomy Reference

Field definitions for `csi_section_code`, `spec_family`, `subfamily`, and `control_function` are defined in `shared_taxonomy.json`. This kernel uses those canonical field definitions.
