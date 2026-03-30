# Taxonomy — Construction Assembly Kernel

## Assembly Type Taxonomy

The kernel classifies assemblies into six types based on their position and function in the building enclosure.

### roof_assembly

Horizontal or near-horizontal assemblies protecting the top of the building enclosure. Includes low-slope membrane roofing (TPO, EPDM, PVC, modified bitumen, built-up) and steep-slope roofing (shingles, tiles, metal panels). Primary control layers: bulk_water_control, thermal_control, weathering_surface.

- CSI sections: 07 30 00 (steep slope), 07 50 00 (membrane)
- Typical layers: membrane, insulation, cover board, vapor retarder, substrate/deck
- Key interfaces: roof_to_wall, parapet_transition, roof_edge, penetration, curb_transition, drain_transition

### wall_assembly

Vertical assemblies forming the sides of the building enclosure. Includes cladding systems, air/water barrier systems, insulation, and interior finishes. Primary control layers: air_control, bulk_water_control, thermal_control, vapor_control.

- CSI sections: 07 25 00 (weather barriers), 07 27 00 (air barriers), 07 40 00 (panels)
- Typical layers: cladding, air space/drainage cavity, sheathing, air/water barrier, insulation, vapor retarder, interior finish
- Key interfaces: roof_to_wall, fenestration_edge, below_grade_transition, expansion_joint

### below_grade_assembly

Assemblies below the ground surface. Includes foundation walls, slabs-on-grade, and below-grade structures. Must resist hydrostatic pressure, soil moisture, and backfill loads. Primary control layers: bulk_water_control, capillary_control, protection_layer.

- CSI sections: 07 10 00 (dampproofing and waterproofing)
- Typical layers: protection board, drainage board, waterproofing membrane, insulation, substrate
- Key interfaces: below_grade_transition

### plaza_assembly

Horizontal assemblies over occupied space supporting pedestrian or vehicular traffic. Combines waterproofing with wearing surface. Zero-leak tolerance because failure affects interior spaces. Primary control layers: bulk_water_control, protection_layer, drainage_plane.

- CSI sections: 07 10 00 (waterproofing), associated with hardscape finishes
- Typical layers: wearing surface (pavers, topping slab), protection/drainage composite, waterproofing membrane, insulation, substrate
- Key interfaces: deck_to_wall, drain_transition, expansion_joint

### vegetated_assembly

Assemblies supporting plant growth on roofs or walls. Adds root barrier, growing media, and drainage/retention layers above a waterproofing assembly. Primary control layers: bulk_water_control, vegetation_support_layer, drainage_plane, protection_layer.

- CSI sections: 07 50 00 (membrane base), associated with vegetated systems
- Typical layers: vegetation, growing media, filter fabric, drainage/retention layer, root barrier, waterproofing membrane, insulation, vapor retarder, substrate
- Key interfaces: roof_to_wall, parapet_transition, drain_transition, penetration

### hybrid_assembly

Assemblies combining characteristics of two or more types. Examples: insulated metal panel systems serving as both wall cladding and air/vapor barrier; inverted roof membrane assemblies (IRMA) with insulation above the membrane.

- Kernel treatment: classified as hybrid with notes documenting which characteristics from which types apply
- Key concern: control-layer assignments may differ from conventional assumptions

## Component Type Taxonomy

Assembly components are classified by function:

| Component Type | Function |
|---|---|
| membrane | Primary water/air control sheet or fluid-applied layer |
| insulation | Thermal control board, batt, or spray material |
| substrate | Structural deck or sheathing receiving assembly layers |
| cover_board | Protective board over insulation, below membrane |
| fastener | Mechanical attachment (screws, plates, clips) |
| adhesive | Bonding agent for adhered systems |
| sealant | Joint sealant for gap and penetration sealing |
| flashing | Sheet material directing water at transitions |
| edge_metal | Perimeter metal at roof edges (fascia, coping, gravel stop) |
| drain | Roof drain, scupper, or overflow device |
| curb | Raised frame for equipment, skylights, or hatches |
| vapor_retarder | Vapor diffusion control sheet or coating |
| air_barrier | Dedicated air control membrane or coating |
| firebreak | Fire-rated barrier or safing within assembly |
