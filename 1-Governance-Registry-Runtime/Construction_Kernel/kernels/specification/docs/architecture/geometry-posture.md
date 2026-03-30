# Geometry Posture — Construction Specification Kernel

## Geometry Context in Specifications

Building geometry directly affects specification requirements for Division 07 systems. Wind uplift zones, roof slope classifications, wall height, parapet dimensions, and penetration density all drive specification variations within the same CSI section.

## Geometry-Dependent Specification Requirements

### Wind Uplift Zones

Roofing specifications divide the roof into zones with different attachment requirements:

- **Field** — interior area with lowest wind uplift pressures
- **Perimeter** — strip along roof edges with higher uplift pressures
- **Corner** — areas near roof corners with highest uplift pressures

Specification requirements for fastener spacing, adhesive application rates, and membrane securement vary by zone. The `geometry_context` field captures which zone a requirement applies to.

### Roof Slope Classification

- **Low-slope** (less than 2:12) — membrane roofing systems, ponding considerations, minimum slope-to-drain requirements
- **Steep-slope** (2:12 and greater) — shingle and panel systems, underlayment requirements, ice dam protection

Slope classification drives which specification sections and requirements apply. A low-slope roof specification includes requirements for positive drainage that do not appear in steep-slope sections.

### Wall Height and Exposure

Tall wall fields (shared geometry context `tall_wall_field`) may trigger enhanced wind load requirements, additional mechanical attachment, and more frequent expansion joints. Specifications for wall systems may include height-dependent requirements.

### Penetration Density

Areas with multiple penetrations (`multi_penetration_field`) require more detailed flashing and sealing specifications. Penetration-dense roof areas may require different membrane reinforcement or additional flashing details.

### Complex Geometry

Complex roof geometry (`complex_roof_geometry`) — multiple ridges, valleys, dormers, or intersecting planes — increases the specification burden for flashing, transitions, and drainage. Specifications may include additional requirements for mock-ups or preconstruction meetings.

### Parapet and Edge Conditions

Large parapet runs (`large_parapet_run`) require expansion joint specifications within the parapet cap, coping attachment requirements, and through-wall flashing coordination.

## Recording Geometry Context

When a specification requirement is geometry-dependent, the kernel records:

1. The requirement with its obligation level and performance criteria
2. The `geometry_context` field using values from `shared_enum_registry.json`
3. The source pointer to the spec clause establishing the geometry dependency
4. `ambiguity_flag: true` if the spec does not clearly delineate zone boundaries

## Geometry Context Is Not Geometric Modeling

This kernel records that specification requirements vary by geometric condition. It does not store coordinates, calculate wind pressures, model drainage paths, or generate zone diagrams. Those functions belong to engineering analysis tools and BIM systems.

## Shared Registry Reference

Geometry context values are defined in `shared_enum_registry.json` under `geometry_contexts`. All geometry context values in this kernel use those canonical enum values.
