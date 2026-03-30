# Control Layer Model — Construction Assembly Kernel

## Definition

Control layers are the functional layers within an assembly that manage the flow of water, air, vapor, heat, fire, and movement through the building enclosure. The 11 control layers defined in the shared registry are the organizing vocabulary for all assembly truth in this kernel.

## The 11 Control Layers

From `Construction_Reference_Intelligence/shared/control_layers.json`:

| # | ID | Name | Function |
|---|---|---|---|
| 1 | bulk_water_control | Bulk Water Control | Stops liquid water (rain, snowmelt, standing water) |
| 2 | capillary_control | Capillary Control | Resists moisture migration through porous materials |
| 3 | air_control | Air Control | Limits uncontrolled air movement through enclosure |
| 4 | vapor_control | Vapor Control | Manages vapor diffusion to prevent condensation |
| 5 | thermal_control | Thermal Control | Manages heat flow (insulation) |
| 6 | fire_smoke_control | Fire and Smoke Control | Limits fire spread and smoke migration |
| 7 | movement_control | Movement Control | Accommodates thermal, structural, seismic movement |
| 8 | weathering_surface | Weathering Surface | Resists UV, wind, precipitation, degradation |
| 9 | drainage_plane | Drainage Plane | Directs incidental moisture down and out |
| 10 | protection_layer | Protection Layer | Shields underlying layers from damage |
| 11 | vegetation_support_layer | Vegetation Support Layer | Supports vegetated assembly growth media and root barrier |

## Continuity Tracking

The kernel tracks control-layer continuity at three levels:

### Assembly-Level Continuity

Each `assembly_system` records continuity status for each control layer it addresses:

```json
{
  "control_layer_continuity": {
    "bulk_water_control": "continuous",
    "air_control": "continuous",
    "thermal_control": "continuous",
    "vapor_control": "continuous"
  }
}
```

### Transition-Level Continuity

Each `transition_condition` records which control layers are maintained across the transition:

```json
{
  "control_layers_maintained": ["bulk_water_control", "air_control", "thermal_control"]
}
```

If a control layer is not listed in `control_layers_maintained`, it is either not present or interrupted at the transition.

### Requirement-Level Continuity

Each `continuity_requirement` defines a rule:

```json
{
  "control_layer_id": "air_control",
  "continuity_type": "must_be_continuous",
  "scope": "All roof-to-wall transitions in ASHRAE climate zones 4-8"
}
```

## Continuity Status Values

| Status | Meaning |
|---|---|
| continuous | Control layer is unbroken through this assembly or across this boundary |
| interrupted | Control layer has a gap or breach (may be intentional or defective) |
| terminated | Control layer ends at this point (e.g., waterproofing terminates at grade) |
| transitioned | Control layer function transfers from one material/system to another |

## Control Layer Relationships

Some control layers are interdependent:
- **air_control + vapor_control**: In cold climates, the air barrier often also serves as the vapor retarder. A breach in air control can cause condensation (vapor control failure).
- **bulk_water_control + drainage_plane**: In wall assemblies, the WRB provides bulk water control while the drainage cavity provides a drainage plane. Both must be continuous.
- **thermal_control + vapor_control**: Vapor retarder position depends on insulation position. Moving insulation changes the dew point location.

## Control Layer Assignment Conflicts

When two layers in the same assembly claim the same control-layer function:
- If intentional (primary + secondary water control), both assignments are recorded with notes.
- If conflicting (two vapor retarders on opposite sides of insulation in a cold climate), the conflict is flagged with `ambiguity_flag: true` and the record remains in `draft` status.

## Limitations

- Control layer IDs are defined in the shared registry. This kernel consumes them; it does not modify them.
- Physical performance of control layers (permeance values, R-values, air leakage rates) belongs to the Material Kernel.
- Control-layer design strategy and best-practice guidance belongs to the Reference Intelligence layer.
