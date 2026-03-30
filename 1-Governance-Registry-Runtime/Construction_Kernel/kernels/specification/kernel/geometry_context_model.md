# Geometry Context Model — Construction Specification Kernel

## Purpose

This model defines how building geometry affects specification requirements for Division 07 systems. Roof slope, wind uplift zones, wall height, penetration density, and parapet configuration all drive specification variations.

## Geometry Context Values

From `shared_enum_registry.json` under `geometry_contexts`:

- `low_slope_roof` — roof slope less than 2:12, membrane roofing applicable
- `steep_slope_roof` — roof slope 2:12 or greater, shingle/panel roofing applicable
- `complex_roof_geometry` — multiple planes, valleys, dormers, or intersecting ridges
- `large_parapet_run` — extended parapet lengths requiring expansion joints
- `multi_penetration_field` — high density of roof or wall penetrations
- `irregular_drainage_geometry` — non-standard drainage paths or ponding conditions
- `tall_wall_field` — wall heights exceeding typical single-story exposure
- `podium_condition` — horizontal surface over occupied space (plaza deck)

## Geometry-Driven Specification Variations

### Wind Uplift Zones (Roofing)

Roofing specifications divide the roof into attachment zones:

| Zone | Location | Specification Impact |
|---|---|---|
| Field | Interior roof area | Base fastener spacing, standard adhesive rate |
| Perimeter | Strip along roof edges | Increased fastener density, enhanced adhesive |
| Corner | Intersection of two edges | Maximum fastener density, fully adhered required |

Requirements for each zone carry `geometry_context` metadata identifying the applicable zone. FM Global I-90 wind uplift ratings and ASCE 7 wind pressure calculations inform these zone-specific requirements.

### Roof Slope

- Low-slope: positive drainage required, minimum 1/4" per foot to drains, cricket/saddle requirements at penetrations
- Steep-slope: underlayment requirements, ice dam protection in cold climates, exposure limitations by slope

### Penetration Density

Areas with multiple penetrations require:
- Individual flashing details for each penetration type
- Minimum spacing requirements between penetrations
- Potential pitch pocket or curb consolidation requirements
- Enhanced inspection requirements

### Parapet Configuration

Large parapet runs require:
- Expansion joints in coping at specified intervals
- Through-wall flashing coordination
- Counterflashing attachment methods
- Parapet cap slope for drainage

### Podium Conditions

Podium decks (waterproofing over occupied space) trigger:
- Zero-tolerance waterproofing requirements
- Flood testing requirements
- Protection board and drainage mat specifications
- Enhanced warranty requirements

## Recording Geometry Context

The `geometry_context` field on requirement records identifies the geometric condition that triggers the requirement. Requirements without geometry context apply regardless of geometry.

When a specification does not differentiate requirements by geometry zone (e.g., specifies uniform fastener spacing without zone distinction), the kernel records the requirement without geometry context and may flag the absence as a gap if zone-specific requirements are expected per standards.
