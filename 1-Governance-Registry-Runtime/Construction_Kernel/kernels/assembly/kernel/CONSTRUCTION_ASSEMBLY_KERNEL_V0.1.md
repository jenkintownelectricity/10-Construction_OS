# Construction Assembly Kernel — V0.1

## Version

- **Version**: 0.1
- **Status**: Initial structured release
- **Date**: 2026-03-17
- **Baseline**: construction-kernel-pass-2

## Identity

- **Kernel ID**: KERN-CONST-ASSY
- **Family**: construction-kernel
- **Role**: Assembly truth kernel
- **Domain Focus**: CSI Division 07 — Building Envelope Systems
- **Registry**: ValidKernel_Registry

## Truth Surface

This kernel owns assembly-domain truth: how building enclosure systems are composed as ordered layer stacks, how control layers are assigned and maintained, and how assemblies connect at transitions, penetrations, edges, and tie-ins.

## Object Model (V0.1)

Ten core object types:

| # | Object | Schema | Purpose |
|---|---|---|---|
| 1 | assembly_system | assembly_system.schema.json | Complete assembly as ordered layer stack |
| 2 | assembly_layer | assembly_layer.schema.json | Individual layer with position and control-layer assignment |
| 3 | assembly_component | assembly_component.schema.json | Discrete component (membrane, insulation, fastener, etc.) |
| 4 | control_layer_assignment | control_layer_assignment.schema.json | Maps assembly to control-layer function |
| 5 | transition_condition | transition_condition.schema.json | Assembly-to-assembly connection at interface zone |
| 6 | penetration_condition | penetration_condition.schema.json | Element passing through assembly |
| 7 | edge_condition | edge_condition.schema.json | Assembly termination at perimeter |
| 8 | tie_in_condition | tie_in_condition.schema.json | Connection at construction boundary |
| 9 | tested_assembly_record | tested_assembly_record.schema.json | Test-validated assembly configuration |
| 10 | continuity_requirement | continuity_requirement.schema.json | Control-layer continuity rule |

## Control Layers (11)

Referenced from shared registry: bulk_water_control, capillary_control, air_control, vapor_control, thermal_control, fire_smoke_control, movement_control, weathering_surface, drainage_plane, protection_layer, vegetation_support_layer.

## Interface Zones (10)

Referenced from shared registry: roof_to_wall, parapet_transition, penetration, fenestration_edge, below_grade_transition, expansion_joint, deck_to_wall, roof_edge, curb_transition, drain_transition.

## Governance

- **Schema validation**: Mandatory. All records must pass JSON Schema validation.
- **Fail-closed**: Incomplete or ambiguous records remain in draft status.
- **Append-only revision**: Records are versioned, never overwritten.
- **Evidence-linked**: Assembly claims should be traceable to evidence.
- **Standards-aware**: References standards by citation, never reproduces text.

## V0.1 Scope

- All 10 object schemas defined with JSON Schema 2020-12
- Doctrine, architecture, and system documentation complete
- Kernel models for all truth surfaces documented
- Example records for TPO roof, roof-to-wall transition, pipe penetration, parapet edge, and fire-rated wall
- Contracts defined for primary truth exchanges
- Maps defined for kernel relationships

## Known Limitations (V0.1)

- No runtime validation service — schema validation is offline
- No automated cross-kernel reference resolution
- No automated continuity verification across assembly boundaries
- Example data is representative, not exhaustive
