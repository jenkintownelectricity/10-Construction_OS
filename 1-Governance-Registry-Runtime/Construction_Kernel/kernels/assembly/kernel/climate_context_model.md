# Climate Context Model — Construction Assembly Kernel

## Purpose

Defines how climate context is recorded on assembly records. Climate affects assembly configuration: vapor retarder position, insulation strategy, drainage requirements, material durability, and wind resistance design.

## Climate Data Recorded

### ASHRAE Climate Zone

A string value (e.g., "4A", "5B", "7") identifying the climate zone per ASHRAE 90.1. Drives prescriptive insulation requirements and vapor control strategy.

### Climate Exposure Flags

From `shared_enum_registry.json#climate_exposure_flags`:

| Flag | Assembly Impact |
|---|---|
| marine_exposure | Corrosion-resistant fasteners and metals; salt-tolerant membranes |
| high_uv | UV-resistant weathering surface; higher reflectance membranes |
| freeze_thaw | Closed-cell insulation below grade; drainage to prevent ice damming |
| coastal_salt | Enhanced corrosion protection; accelerated maintenance cycles |
| high_wind | Higher wind uplift ratings; enhanced edge securement; fully adhered systems |
| high_humidity | Vapor control strategy critical; mold-resistant substrates |
| severe_precipitation | Enhanced drainage design; redundant water control; higher slope requirements |

### Exposure Class

From `shared_taxonomy.json#exposure_class`:
- sheltered — minimal environmental stress
- moderate — typical urban/suburban exposure
- severe — significant climate stress (coastal, mountain, high wind)
- extreme — maximum climate exposure requiring highest-performance assemblies

## Climate Context Object

Recorded on `assembly_system` records:

```json
{
  "climate_context": {
    "climate_zone": "5A",
    "exposure_flags": ["freeze_thaw", "high_wind"],
    "exposure_class": "severe"
  }
}
```

## Climate-Driven Control-Layer Decisions

### Vapor Control

| Climate | Vapor Retarder Position | Typical Permeance |
|---|---|---|
| Cold (zones 5-8) | Warm side (interior of insulation) | Class I or II (< 1.0 perm) |
| Hot-humid (zones 1A-3A) | Exterior side or omitted | Variable or Class III |
| Mixed (zone 4A) | Requires analysis | Smart retarder (variable perm) |
| Marine (any zone) | Per analysis | Salt exposure may affect retarder selection |

### Thermal Control

| Climate | ASHRAE 90.1 Roof R-value | Wall R-value (CI) |
|---|---|---|
| Zone 1 | R-20 ci | R-5.7 ci |
| Zone 4 | R-25 ci | R-7.6 ci |
| Zone 7 | R-35 ci | R-13.0 ci |

Values are approximate and referenced by citation to ASHRAE 90.1 tables. Exact values must be verified against the current edition.

### Water Control

- High precipitation zones require enhanced drainage plane design
- Freeze-thaw zones require ice-and-water shield at eaves and valleys (steep slope)
- Coastal zones require corrosion-resistant flashing materials

## Limitations

- Climate context is metadata, not analysis. The kernel does not perform hygrothermal simulation.
- Climate zone assignment is project-specific. The kernel records the zone; it does not determine it.
- Future climate projections and climate change adaptation are outside kernel scope.
