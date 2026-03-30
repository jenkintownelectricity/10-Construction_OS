# Continuity Model — Construction Assembly Kernel

## Definition

Control-layer continuity is the unbroken maintenance of a control function across an assembly, across transitions between assemblies, through penetrations, and at terminations. The continuity model defines rules for when control layers must be continuous, may be interrupted, must terminate, or must transition.

## Continuity Types

| Type | Meaning |
|---|---|
| must_be_continuous | Control layer must be unbroken across the specified scope. Any interruption is a defect. |
| may_be_interrupted | Control layer may have intentional interruptions within the scope (e.g., weep holes in drainage plane). |
| must_terminate | Control layer must end at a defined location with a proper termination detail. |
| must_transition | Control layer function must transfer from one material/system to another at the boundary. |

## Continuity Requirements by Control Layer

### bulk_water_control — Must be continuous

Water control must be unbroken from the highest point of the enclosure to the lowest. Every transition, penetration, and edge must maintain water control continuity. There is no acceptable interruption in the primary water control layer.

**Scope**: Entire building enclosure — roof, walls, below-grade, all transitions.

### air_control — Must be continuous

Air barrier continuity is required by most energy codes (ASHRAE 90.1, IECC). The air barrier must be continuous across walls, roofs, and floors, with sealed transitions at every interface zone.

**Scope**: Entire building enclosure. Continuity must be demonstrable by tracing the air barrier on any building section.

### vapor_control — Varies by climate

Vapor control continuity requirements depend on climate zone and assembly configuration:
- Cold climates: vapor retarder must be continuous on the warm side of insulation
- Hot-humid climates: vapor retarder position and continuity depend on analysis
- Mixed climates: smart vapor retarders may allow variable permeance

**Scope**: Climate-dependent. Continuity requirement is conditional.

### thermal_control — Must be continuous (with allowed thermal bridges)

Continuous insulation (ci) requirements per ASHRAE 90.1 demand unbroken thermal control. However, structural attachments (shelf angles, clips, fasteners) create thermal bridges that are analytically acceptable within defined limits.

**Scope**: Continuous across assembly field. Thermal bridges at attachments are documented, not prohibited.

### fire_smoke_control — Must be continuous at rated boundaries

Fire-rated assemblies must maintain their rating continuously along the rated boundary. Penetrations through rated assemblies require firestopping. Joints require fire-rated joint systems.

**Scope**: Along each rated boundary as defined by the building code.

### drainage_plane — Must be continuous within wall assemblies

The drainage plane must provide an unbroken path from the top of the wall to the base, directing water to weeps or through-wall flashings.

**Scope**: Each wall assembly from top to base. Interruptions at floor lines require through-wall flashing.

## Continuity Across Boundaries

### At Transitions

When two assemblies meet (e.g., roof-to-wall), the transition_condition record documents which control layers are maintained. Continuity requirements define which layers must be maintained at each transition type.

### At Penetrations

Every penetration interrupts control layers. The penetration_condition record documents which layers are affected and the seal method. Continuity is restored by the seal method.

### At Edges and Terminations

Edge conditions document where control layers terminate. Continuity requirements of type `must_terminate` define proper termination details.

## Continuity Verification

Continuity can be verified by:
1. **Drawing review**: Tracing each control layer on building sections and details
2. **Field inspection**: Visual and instrumental verification during construction
3. **Testing**: Air leakage testing (ASTM E2357), water testing (ASTM E331)
4. **Thermal imaging**: Identifying thermal control discontinuities

The kernel records continuity status. Verification procedures and results are linked as evidence.
