# Geometry Posture — Construction Assembly Kernel

## Principle

Geometry affects assembly design. Roof slope, parapet height, penetration density, wall height, and building shape all influence assembly configuration, attachment requirements, and risk exposure. The kernel records geometry context as metadata — it does not store geometric models or perform structural analysis.

## Geometry-Driven Assembly Decisions

### Roof Slope

- **Low-slope roofs (< 2:12)**: Require fully waterproof membrane systems (TPO, EPDM, PVC, modified bitumen, built-up). Positive drainage to drains and scuppers. Ponding water risk at slopes below 1/4":12".
- **Steep-slope roofs (> 4:12)**: Shed water by gravity. Underlayment plus shingles, tiles, or metal panels. Water-shedding rather than waterproof.
- **Transitional slope (2:12 to 4:12)**: Requires careful system selection. Some membrane systems rated for steep slope; some steep-slope materials rated for lower slope with enhanced underlayment.

### Parapet Height

- **Low parapets (< 24")**: May not provide adequate height for membrane termination above anticipated water line. Code minimum heights apply.
- **Tall parapets**: Increased wind exposure on the interior face. Through-wall flashing required. Coping must accommodate thermal movement.

### Penetration Density

- **High penetration density**: Multiplies risk. Each penetration interrupts control layers. Clustered penetrations (mechanical equipment areas) may require curbed platforms to consolidate penetrations above the membrane plane.
- **Low penetration density**: Standard individual penetration details may suffice.

### Wall Height

- **Tall wall fields**: Wind pressure increases with height. Cladding attachment spacing decreases at upper floors. Air barrier must resist greater pressure differentials.
- **Ground-level walls**: Splash-back zone requires enhanced water control at base of wall.

### Building Shape

- **Complex roof geometry**: Valleys, ridges, and intersecting planes create concentrated water flow paths. Cricket and saddle requirements at roof-to-wall intersections.
- **Re-entrant corners**: Wind acceleration at inside corners increases uplift loads.

## Geometry Context Values

From `shared_enum_registry.json#geometry_contexts`:

| Context | Assembly Impact |
|---|---|
| low_slope_roof | Membrane waterproofing required; drainage design critical |
| steep_slope_roof | Water-shedding system; underlayment quality critical |
| complex_roof_geometry | Multiple transition conditions; valley and ridge details |
| large_parapet_run | Expansion joints in coping; through-wall flashing |
| multi_penetration_field | Consolidated curb strategy; increased inspection density |
| irregular_drainage_geometry | Custom drainage design; potential ponding analysis |
| tall_wall_field | Enhanced wind resistance; air barrier pressure requirements |
| podium_condition | Plaza waterproofing over occupied space; zero-leak tolerance |

## Geometry Context in Kernel Objects

### assembly_system.geometry_context

Records geometric conditions affecting the assembly:

```json
{
  "geometry_contexts": ["low_slope_roof", "multi_penetration_field"],
  "notes": "Mechanical equipment area with 24 penetrations per 100 SF"
}
```

## Limitations

- The kernel records geometry context; it does not perform structural analysis or wind load calculations.
- Drainage calculations, slope verification, and ponding analysis are outside kernel scope.
- CAD geometry, BIM models, and coordinate data are not stored in the kernel.
- Geometry-driven performance intelligence (e.g., failure rates by roof complexity) belongs to the Reference Intelligence layer.
