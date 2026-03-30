# Division 07 Alignment — Construction Specification Kernel

## Division 07 as Enclosure Control-Layer System

CSI Division 07 — Thermal and Moisture Protection — encompasses the building envelope systems that form the control layers separating conditioned interior space from the exterior environment. This kernel maps Division 07 specification sections to the control layers and interface zones defined in the shared registries.

## Section-to-Control-Layer Mapping

| CSI Section | Title | Primary Control Layers |
|---|---|---|
| 07 10 00 | Dampproofing and Waterproofing | bulk_water_control, capillary_control |
| 07 13 00 | Sheet Waterproofing | bulk_water_control, capillary_control |
| 07 14 00 | Fluid-Applied Waterproofing | bulk_water_control, capillary_control |
| 07 21 00 | Thermal Insulation | thermal_control |
| 07 22 00 | Roof and Deck Insulation | thermal_control, protection_layer |
| 07 25 00 | Weather Barriers | air_control, bulk_water_control |
| 07 26 00 | Vapor Retarders | vapor_control |
| 07 27 00 | Air Barriers | air_control |
| 07 31 00 | Shingles and Shakes | weathering_surface, bulk_water_control |
| 07 41 00 | Roof Panels | weathering_surface, bulk_water_control |
| 07 42 00 | Wall Panels | weathering_surface, bulk_water_control |
| 07 46 00 | Siding | weathering_surface |
| 07 51 00 | Built-Up Bituminous Roofing | bulk_water_control, weathering_surface |
| 07 52 00 | Modified Bituminous Membrane Roofing | bulk_water_control, weathering_surface |
| 07 53 00 | Elastomeric Membrane Roofing | bulk_water_control, weathering_surface |
| 07 54 00 | Thermoplastic Membrane Roofing | bulk_water_control, weathering_surface |
| 07 55 00 | Protected Membrane Roofing | bulk_water_control, protection_layer |
| 07 56 00 | Fluid-Applied Roofing | bulk_water_control, weathering_surface |
| 07 60 00 | Flashing and Sheet Metal | bulk_water_control, drainage_plane |
| 07 62 00 | Sheet Metal Flashing and Trim | bulk_water_control, drainage_plane |
| 07 65 00 | Flexible Flashing | bulk_water_control, drainage_plane |
| 07 70 00 | Roof and Wall Specialties | movement_control, weathering_surface |
| 07 72 00 | Roof Accessories | bulk_water_control, movement_control |
| 07 84 00 | Firestopping | fire_smoke_control |
| 07 86 00 | Smoke Seals | fire_smoke_control |
| 07 92 00 | Joint Sealants | air_control, bulk_water_control, movement_control |
| 07 95 00 | Expansion Joint Cover Assemblies | movement_control |

## Interface Zone Relevance

Division 07 sections are most specification-intensive at interface zones where control layer continuity is challenged. The shared `interface_zones.json` registry defines ten canonical interface zones. Specification sections must explicitly address transitions at these zones or flag gaps via `ambiguity_flag`.

## Multi-Layer Sections

Many Division 07 sections serve multiple control layers simultaneously. For example, a thermoplastic membrane roofing section (07 54 00) serves both `bulk_water_control` and `weathering_surface`. The `control_layers_served` array in the specification section schema captures this multi-layer function.
