# Climate Posture — Construction Specification Kernel

## Climate Context in Specifications

Climate conditions directly affect specification requirements for Division 07 building envelope systems. Vapor retarder class, insulation R-values, air barrier performance thresholds, and material selection requirements all vary by climate zone and exposure conditions.

## Climate-Dependent Specification Requirements

### Vapor Retarder Class

IBC and ASHRAE 90.1 require different vapor retarder classes based on climate zone:

- Climate Zones 5, 6, 7, 8 (cold/very cold): Class I or II vapor retarder required on warm side
- Climate Zone 4C (marine): Class I or II vapor retarder required
- Climate Zones 1, 2, 3, 4A, 4B (warm/mixed): Vapor retarder class varies by assembly analysis

Specification requirements referencing vapor retarder class carry a `climate_context` field identifying the applicable climate zone.

### Thermal Insulation Values

Continuous insulation R-values specified per ASHRAE 90.1 vary by climate zone. Specification requirements for roof insulation, wall insulation, and below-grade insulation carry climate-zone-dependent performance criteria.

### Air Barrier Performance

While air barrier requirements apply in all climate zones per IBC, specification performance thresholds may be more stringent in extreme climates. The `climate_context` field captures these zone-specific requirements.

### Material Selection

Climate exposure flags from `shared_enum_registry.json` affect material suitability:

- `marine_exposure` — corrosion-resistant fasteners, marine-grade coatings required
- `high_uv` — UV-stable membrane surfaces, reflective coating requirements
- `freeze_thaw` — freeze-thaw-resistant materials, drainage requirements to prevent ponding
- `coastal_salt` — salt-spray-resistant materials and coatings
- `high_wind` — enhanced securement, higher wind uplift ratings
- `high_humidity` — mold-resistant materials, enhanced vapor management
- `severe_precipitation` — enhanced waterproofing, higher drainage capacity

## Recording Climate Context

When a specification requirement is climate-dependent, the kernel records:

1. The requirement itself with its obligation level and performance criteria
2. The `climate_context` field identifying the applicable climate zone or exposure flag
3. The source pointer to the spec clause that establishes the climate dependency
4. `ambiguity_flag: true` if the spec does not clearly state which climate zones apply

## Climate Context Is Not Climate Modeling

This kernel records that a specification requirement varies by climate zone. It does not perform hygrothermal analysis, predict condensation risk, or model moisture transport. Those functions belong to engineering analysis tools and the intelligence layer.

## Shared Registry Reference

Climate exposure flags are defined in `shared_enum_registry.json` under `climate_exposure_flags`. All climate context values in this kernel use those canonical enum values.
