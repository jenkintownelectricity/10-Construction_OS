# Geometry Posture — Construction Material Kernel

## Geometry Context for Materials

Building geometry affects material requirements and performance expectations. Roof slope, wall orientation, substrate geometry, and detail geometry influence which material properties are critical. This kernel records geometry context as metadata on material records — it does not store geometric models.

## Geometry Factors Affecting Material Selection

| Geometry Factor | Material Impact | Kernel Coverage |
|---|---|---|
| Roof slope (low-slope vs steep) | Determines membrane vs shingle material class | Records slope applicability metadata |
| Wall orientation (vertical vs inclined) | Affects drainage plane material requirements | Records orientation-specific properties |
| Substrate curvature | Affects material flexibility requirements | Records elongation and flexibility properties |
| Joint width and movement | Determines sealant movement capacity needs | Records movement capacity properties |
| Penetration size and spacing | Affects flashing material selection | Records flashing material properties |
| Building height (wind zone) | Affects mechanical property requirements | Records wind uplift resistance properties |

## Geometry Context in Material Records

Material performance records include an optional `geometry_context` field:

- Roof slope classification (low_slope, steep_slope, vertical, below_grade)
- Application orientation (horizontal, vertical, inverted)
- Substrate type context (concrete, metal_deck, wood, gypsum)
- Movement joint classification (static, dynamic, seismic)

## What This Kernel Does

- Records material properties with geometry-relevant context
- Tags materials with applicable geometry configurations
- Records substrate-specific adhesion and compatibility data
- Stores geometry-influenced property values (e.g., different permeance for horizontal vs vertical)

## What This Kernel Does Not Do

- Does not store drawings, CAD geometry, or BIM objects
- Does not calculate geometric quantities (areas, lengths, slopes)
- Does not model water flow paths or drainage patterns
- Does not determine geometric detailing sequences (assembly truth)
- Does not perform structural analysis of material under geometric loads

## Geometry and Assembly Boundary

Geometry context in this kernel describes when material properties apply. Geometric configuration of materials within assemblies (layer order, overlap dimensions, fastener patterns) belongs to the Assembly Kernel. This kernel provides material properties that the Assembly Kernel uses within geometric contexts.

## Typical Geometry-Dependent Material Decisions

| Decision | Material Data Provided | Decision Owner |
|---|---|---|
| Membrane type for 1/4:12 slope | Low-slope membrane properties | Assembly / Specification Kernel |
| Sealant for 1-inch expansion joint | Movement capacity, elongation | Specification Kernel |
| Insulation for cathedral ceiling | R-value, vapor permeance | Assembly Kernel |
| Flashing at curved parapet | Elongation, formability | Assembly Kernel |
