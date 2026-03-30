# Geometry Context Model — Construction Assembly Kernel

## Purpose

Defines how geometry context is recorded on assembly records. Building geometry affects assembly design: roof slope determines system type, parapet length affects expansion joint spacing, penetration density drives risk, and wall height affects wind loads.

## Geometry Context Values

From `shared_enum_registry.json#geometry_contexts`:

| Context | Description | Assembly Impact |
|---|---|---|
| low_slope_roof | Roof slope < 2:12 | Requires membrane waterproofing; positive drainage design critical |
| steep_slope_roof | Roof slope > 4:12 | Water-shedding system (shingles, tiles, metal panels); underlayment is secondary water control |
| complex_roof_geometry | Multiple slopes, valleys, ridges, intersecting planes | Multiple transition conditions; concentrated water flow paths |
| large_parapet_run | Extended parapet length | Expansion joints required in coping; thermal movement accommodation |
| multi_penetration_field | High density of penetrations | Elevated risk; consider consolidated curb platforms |
| irregular_drainage_geometry | Non-uniform slopes, saddles, sumps | Custom drainage design; potential ponding areas |
| tall_wall_field | Wall height exceeding typical single-story | Higher wind pressures; reduced attachment spacing at upper levels |
| podium_condition | Horizontal assembly over occupied space | Zero-leak tolerance; enhanced waterproofing and drainage |

## Geometry Context Object

Recorded on `assembly_system` records:

```json
{
  "geometry_context": {
    "geometry_contexts": ["low_slope_roof", "multi_penetration_field"],
    "notes": "Mechanical equipment area — 18 penetrations within 400 SF"
  }
}
```

## Geometry-Driven Design Rules

### Slope and Drainage

- Low-slope roofs require minimum 1/4" per foot slope to drains (IBC 1502.1)
- Ponding risk exists where effective slope approaches zero after deflection
- Tapered insulation systems create slope; layer stack includes tapered boards
- Cricket/saddle assemblies required at roof-to-wall intersections wider than 24" (varies by code)

### Penetration Geometry

- Individual penetrations spaced > 24" apart: standard individual details
- Clustered penetrations < 12" apart: consider raised curb platform to consolidate above membrane
- Penetrations near roof edges or low points: elevated risk due to water concentration

### Edge and Perimeter

- Corner zones (per FM wind zone diagram): highest wind uplift loads; enhanced attachment required
- Perimeter zones: intermediate wind loads; attachment spacing reduced vs. field of roof
- Large parapet runs (> 100 linear feet): expansion joints in coping and counter-flashing

### Wall Geometry

- Wall height > 30 feet: wind pressure differential increases; air barrier and cladding attachment must be designed for higher loads
- Recessed areas and overhangs: altered wind pressure patterns; may reduce or increase local loads

## Geometry and Risk

Geometry directly affects interface risk levels:
- Multi-penetration fields increase the probability of at least one seal failure
- Complex roof geometry multiplies the number of transition conditions
- Podium conditions make any water control failure immediately consequential

## Limitations

- The kernel records geometry context as metadata. It does not store coordinates, dimensions, or 3D models.
- Structural load calculations, wind pressure analysis, and drainage flow modeling are outside kernel scope.
- Geometry-to-performance correlation intelligence belongs to the Reference Intelligence layer.
