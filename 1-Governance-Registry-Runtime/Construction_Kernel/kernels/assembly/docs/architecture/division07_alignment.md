# Division 07 Alignment — Construction Assembly Kernel

## Organizing Principle

CSI Division 07 — Thermal and Moisture Protection — is organized in this kernel by control-layer function, not by product type. Each Division 07 subsection maps to one or more control layers and assembly types.

## Division 07 Subsection Mapping

### 07 10 00 — Dampproofing and Waterproofing

- **Control layers**: bulk_water_control, capillary_control, drainage_plane
- **Assembly types**: below_grade_assembly, plaza_assembly
- **Kernel objects**: assembly_system (below-grade walls, foundation), assembly_layer (membrane, drainage board, protection board)
- **Key interface zones**: below_grade_transition

### 07 20 00 — Thermal Protection

- **Control layers**: thermal_control
- **Assembly types**: roof_assembly, wall_assembly, below_grade_assembly
- **Kernel objects**: assembly_layer (rigid insulation, spray foam, mineral fiber), assembly_component (insulation, cover_board)
- **Key concerns**: Continuous insulation position relative to vapor control; thermal bridging at fasteners

### 07 25 00 — Weather Barriers

- **Control layers**: bulk_water_control, drainage_plane
- **Assembly types**: wall_assembly
- **Kernel objects**: assembly_layer (fluid-applied WRB, sheet WRB), assembly_component (membrane)
- **Key interface zones**: fenestration_edge, roof_to_wall

### 07 27 00 — Air Barriers

- **Control layers**: air_control
- **Assembly types**: wall_assembly, roof_assembly
- **Kernel objects**: assembly_layer (self-adhered membrane, fluid-applied barrier), control_layer_assignment
- **Key concerns**: Continuity at transitions, penetrations, and fenestration edges

### 07 30 00 — Steep Slope Roofing

- **Control layers**: weathering_surface, bulk_water_control, thermal_control
- **Assembly types**: roof_assembly
- **Kernel objects**: assembly_system (steep-slope configurations), assembly_layer (underlayment, shingles, tiles, panels)

### 07 50 00 — Membrane Roofing

- **Control layers**: bulk_water_control, weathering_surface, thermal_control, air_control
- **Assembly types**: roof_assembly, vegetated_assembly
- **Kernel objects**: assembly_system (TPO, EPDM, PVC, modified bitumen, built-up), assembly_layer (membrane, insulation, cover board, vapor retarder)
- **Key interface zones**: roof_to_wall, parapet_transition, penetration, roof_edge, curb_transition, drain_transition

### 07 60 00 — Flashing and Sheet Metal

- **Control layers**: bulk_water_control, movement_control, drainage_plane
- **Assembly types**: All assembly types at transitions and edges
- **Kernel objects**: transition_condition, edge_condition, assembly_component (flashing, edge_metal)
- **Key interface zones**: roof_to_wall, parapet_transition, roof_edge

### 07 70 00 — Roof and Wall Specialties

- **Control layers**: Multiple — depends on specialty item
- **Kernel objects**: penetration_condition, edge_condition, assembly_component (curb, drain, vent)
- **Key interface zones**: curb_transition, drain_transition, penetration

### 07 80 00 — Fire and Smoke Protection

- **Control layers**: fire_smoke_control
- **Assembly types**: wall_assembly, roof_assembly
- **Kernel objects**: tested_assembly_record, assembly_component (firebreak), continuity_requirement
- **Key standards**: NFPA 285, ASTM E119, UL 263

### 07 90 00 — Joint Protection

- **Control layers**: movement_control, bulk_water_control, air_control
- **Assembly types**: All assembly types at joints
- **Kernel objects**: transition_condition, tie_in_condition, assembly_component (sealant)
- **Key interface zones**: expansion_joint

## Control-Layer Coverage by Subsection

| Control Layer | 07 10 | 07 20 | 07 25 | 07 27 | 07 30 | 07 50 | 07 60 | 07 70 | 07 80 | 07 90 |
|---|---|---|---|---|---|---|---|---|---|---|
| bulk_water_control | X | | X | | X | X | X | | | X |
| air_control | | | | X | | X | | | | X |
| vapor_control | | X | | | | X | | | | |
| thermal_control | | X | | | X | X | | | | |
| fire_smoke_control | | | | | | | | | X | |
| weathering_surface | | | | | X | X | X | X | | |
| drainage_plane | X | | X | | | | X | | | |
| movement_control | | | | | | | X | | | X |
| protection_layer | X | | | | | X | | X | | |
