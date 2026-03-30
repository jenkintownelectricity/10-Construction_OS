# Assembly Model — Construction Assembly Kernel

## Definition

An assembly system is an ordered stack of layers, each with a defined position, control-layer assignment, material reference, and attachment method. The assembly system is the primary organizing unit of this kernel. Assemblies are not product lists — they are functional systems defined by how their layers work together to maintain control-layer continuity.

## Assembly Structure

### Layer Stack

Every assembly system contains an ordered array of layers numbered from exterior (position 1) to interior (position N):

```
Position 1 (outermost): Weathering surface / membrane
Position 2: Cover board (if present)
Position 3: Insulation
Position 4: Vapor retarder (if present)
Position 5: Substrate / deck
Position N (innermost): Interior finish or structural element
```

The number and type of layers varies by assembly type. A simple single-ply roof may have 4-5 layers. A vegetated roof may have 9-10 layers. A rainscreen wall may have 7-8 layers.

### Layer Properties

Each layer records:

| Property | Required | Description |
|---|---|---|
| layer_id | Yes | Unique identifier for this layer |
| position | Yes | Integer position in stack (1 = outermost) |
| control_layer_id | Yes | Which control layer this layer serves |
| material_ref | Yes | Pointer to Material Kernel entry |
| status | Yes | active, draft, or deprecated |
| attachment_method | No | How this layer is attached (mechanically_attached, fully_adhered, etc.) |
| thickness | No | Layer thickness (informational) |

### Multi-Function Layers

A single physical layer may serve multiple control-layer functions. For example:
- A self-adhered sheet membrane may serve both `bulk_water_control` and `air_control`
- A closed-cell spray foam may serve both `thermal_control` and `vapor_control`
- A modified bitumen cap sheet may serve `bulk_water_control` and `weathering_surface`

When a layer serves multiple functions, it receives multiple control_layer_assignment records.

## Assembly System Properties

| Property | Required | Description |
|---|---|---|
| system_id | Yes | Unique system identifier |
| title | Yes | Human-readable assembly name |
| assembly_type | Yes | roof, wall, below_grade, plaza, vegetated, hybrid |
| status | Yes | active, draft, deprecated |
| layers | No | Array of assembly_layer objects |
| control_layer_continuity | No | Map of control_layer_id to continuity status |
| interface_zones | No | Array of interface zone IDs this assembly encounters |
| climate_context | No | Climate zone, exposure flags, exposure class |
| geometry_context | No | Geometry context values |
| tested_assembly_refs | No | Pointers to tested assembly records |
| standards_refs | No | Applicable standards by reference ID |
| warranty_posture | No | Warranty classification |

## Assembly Type Examples

### Roof Assembly (TPO)

Layers (exterior to interior): TPO membrane (bulk_water_control, weathering_surface) -> polyiso cover board (protection_layer) -> polyiso insulation (thermal_control) -> vapor retarder (vapor_control) -> steel deck (substrate).

### Wall Assembly (Rainscreen)

Layers (exterior to interior): metal panel cladding (weathering_surface) -> air cavity with drainage mat (drainage_plane) -> sheathing + fluid-applied WRB (bulk_water_control, air_control) -> steel studs + mineral fiber insulation (thermal_control) -> interior gypsum (vapor_control if vapor-retarder-coated).

### Below-Grade Assembly

Layers (exterior to interior): protection board (protection_layer) -> drainage board (drainage_plane) -> fluid-applied waterproofing (bulk_water_control) -> rigid insulation (thermal_control) -> concrete foundation wall (substrate).

## Relationship to Other Objects

- `assembly_layer` — contained within assembly_system
- `control_layer_assignment` — references assembly_system by assembly_ref
- `transition_condition` — references assembly_system as from_assembly_ref or to_assembly_ref
- `penetration_condition` — references assembly_system by assembly_ref
- `edge_condition` — references assembly_system by assembly_ref
- `tested_assembly_record` — references assembly_system by assembly_ref
