# Geometry Context Model — Construction Material Kernel

## Purpose

Building geometry affects which material properties are critical and how materials perform. This model defines how geometry context is recorded as metadata on material records.

## Geometry Parameters

| Parameter | Values | Material Relevance |
|---|---|---|
| Slope classification | low_slope, steep_slope, vertical, below_grade | Determines membrane type, drainage behavior |
| Application orientation | horizontal, vertical, overhead, inverted | Affects application method, gravity drainage |
| Substrate type | concrete, metal_deck, wood, gypsum, masonry | Affects adhesion, fastening, compatibility |
| Movement classification | static, dynamic, seismic | Determines sealant movement capacity needs |
| Exposure position | exposed, concealed, buried | Affects UV and weathering requirements |
| Building height zone | low_rise, mid_rise, high_rise | Affects wind uplift requirements |

## Geometry Context in Records

The optional `geometry_context` field in performance records may include:

- **slope** — applicable slope classification
- **orientation** — installation orientation
- **substrate** — substrate type for adhesion/compatibility data
- **exposure** — exposure position
- **height_zone** — building height classification

## Geometry-Dependent Material Requirements

| Geometry | Critical Properties | Rationale |
|---|---|---|
| Low-slope roof (< 2:12) | Permeance, ponding resistance, UV resistance | Water does not drain rapidly |
| Steep-slope roof (> 4:12) | Wind uplift, sliding resistance | Gravity and wind forces |
| Vertical wall | Adhesion, sag resistance | Must resist gravity during application |
| Below grade | Hydrostatic resistance, chemical resistance | Soil contact, water pressure |
| Expansion joint | Elongation > 50%, recovery, fatigue | Repeated movement cycles |
| High-rise exterior | Wind uplift resistance, impact resistance | Elevated wind pressures |

## Slope and Material Class Mapping

| Slope Range | Typical Material Classes |
|---|---|
| 0:12 to 2:12 (low slope) | thermoplastic, thermoset, bituminous |
| 2:12 to 4:12 (transition) | thermoplastic, bituminous, metallic |
| 4:12 and above (steep) | metallic, composite, cementitious |
| Vertical | fluid_applied, sheet_applied, metallic |
| Below grade | bituminous, fluid_applied, sheet_applied |

## Rules

1. Geometry context is metadata — it tags when properties apply, not what they are
2. Geometry-dependent property values must state the geometric conditions
3. The kernel does not design geometric details (assembly truth)
4. Substrate-specific adhesion data references both the material and substrate type
5. Geometric modeling and spatial calculations are outside kernel scope
