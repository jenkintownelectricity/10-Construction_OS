# Interface Model — Construction Assembly Kernel

## Purpose

Defines how assemblies address the 10 interface zones. Each interface zone represents a location where assemblies meet, terminate, or are penetrated — the highest-risk locations in the building enclosure.

## Interface Zone Coverage

### 1. roof_to_wall

**Assemblies involved**: roof_assembly + wall_assembly

**Control layers that must transition**: bulk_water_control (roof membrane to wall WRB), air_control (roof air barrier to wall air barrier), thermal_control (roof insulation to wall insulation), vapor_control (if present in both assemblies).

**Kernel objects**: transition_condition (primary), assembly_layer (flashing layers), assembly_component (flashing, sealant).

**Typical risk level**: critical

### 2. parapet_transition

**Assemblies involved**: roof_assembly + wall_assembly (parapet section)

**Control layers**: Roof membrane extends up parapet face. Air barrier wraps parapet. Insulation may be on exterior or interior of parapet. Coping provides top weathering surface.

**Kernel objects**: transition_condition, edge_condition (coping at top), assembly_component (flashing, coping, sealant).

**Typical risk level**: critical

### 3. penetration

**Assemblies involved**: Any single assembly penetrated by an element

**Control layers affected**: Depends on penetration depth. A pipe through a roof membrane interrupts bulk_water_control, potentially air_control and thermal_control.

**Kernel objects**: penetration_condition (primary), assembly_component (boot, sleeve, sealant).

**Typical risk level**: high to critical (density-dependent)

### 4. fenestration_edge

**Assemblies involved**: wall_assembly + fenestration frame

**Control layers**: air_control (air barrier must seal to frame), bulk_water_control (flashing sequence at head, jamb, sill), thermal_control (insulation return at frame).

**Kernel objects**: transition_condition, assembly_component (flashing, sealant, backer rod).

**Typical risk level**: high

### 5. below_grade_transition

**Assemblies involved**: wall_assembly + below_grade_assembly

**Control layers**: bulk_water_control transitions from weather barrier to waterproofing at or below grade. Protection layer begins. Drainage plane may transition to drainage board.

**Kernel objects**: transition_condition, assembly_component (transition flashing, termination bar).

**Typical risk level**: high

### 6. expansion_joint

**Assemblies involved**: Two sections of same assembly type separated by designed movement

**Control layers**: All control layers must span the joint while accommodating movement. Fire_smoke_control may be required at rated joints.

**Kernel objects**: transition_condition, assembly_component (expansion joint cover, sealant, fire barrier).

**Typical risk level**: high

### 7. deck_to_wall

**Assemblies involved**: plaza_assembly + wall_assembly

**Control layers**: bulk_water_control (waterproofing turns up wall), protection_layer, drainage_plane.

**Kernel objects**: transition_condition, assembly_component (flashing, sealant).

**Typical risk level**: high

### 8. roof_edge

**Assemblies involved**: roof_assembly at perimeter

**Control layers**: bulk_water_control terminates at edge. weathering_surface terminates. Wind uplift loads are highest at edges and corners.

**Kernel objects**: edge_condition (primary), assembly_component (edge_metal, fascia, coping).

**Typical risk level**: medium to high

### 9. curb_transition

**Assemblies involved**: roof_assembly + curb element

**Control layers**: Membrane transitions vertically up curb. Must maintain water and air control at three-dimensional intersection.

**Kernel objects**: transition_condition, penetration_condition (if equipment passes through curb), assembly_component (curb, flashing).

**Typical risk level**: high

### 10. drain_transition

**Assemblies involved**: roof_assembly + drain hardware

**Control layers**: bulk_water_control transitions from membrane to drain body. Clamping ring creates seal.

**Kernel objects**: transition_condition, assembly_component (drain, clamping ring, sealant).

**Typical risk level**: medium

## Interface Completeness Check

A fully documented assembly system should have interface conditions recorded for every interface zone it encounters. An assembly system with `interface_zones: ["roof_to_wall", "penetration", "roof_edge"]` should have corresponding transition_condition and/or penetration_condition records for each.
