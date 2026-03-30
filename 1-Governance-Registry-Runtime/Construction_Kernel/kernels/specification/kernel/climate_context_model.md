# Climate Context Model — Construction Specification Kernel

## Purpose

This model defines how climate conditions affect specification requirements for Division 07 building envelope systems. Climate zone and exposure conditions drive variations in vapor retarder class, insulation values, material selection, and performance thresholds.

## Climate Context Fields

### Climate Zone

ASHRAE climate zones (e.g., "4A", "5B", "7") classify geographic locations by heating degree days, cooling degree days, and moisture regime. Specification requirements that vary by climate zone carry the applicable zone in `climate_context`.

### Climate Exposure Flags

From `shared_enum_registry.json`, exposure flags identify specific environmental stressors:

- `marine_exposure` — salt air and spray corrosion risk
- `high_uv` — elevated ultraviolet radiation degrading exposed membranes
- `freeze_thaw` — cyclic freezing and thawing causing material fatigue
- `coastal_salt` — salt deposition on building surfaces
- `high_wind` — sustained or gust wind loads above typical design
- `high_humidity` — elevated ambient humidity affecting moisture management
- `severe_precipitation` — heavy rain, snow, or ice loading

## Climate-Driven Specification Variations

### Vapor Retarder Requirements
- Cold climates (Zones 5-8): Class I or II vapor retarder on warm-in-winter side
- Mixed climates (Zone 4): Vapor retarder class depends on assembly analysis
- Hot-humid climates (Zones 1-3): Vapor retarder may be contraindicated on interior
- Marine climates (Zone 4C): Special consideration for moisture drive direction

### Insulation R-Values
Minimum R-values per ASHRAE 90.1 increase with climate zone number. Specification requirements for continuous insulation, cavity insulation, and roof insulation carry climate-zone-dependent values.

### Air Barrier Requirements
Air barrier performance thresholds are consistent across climate zones per IBC, but specifications may include enhanced air tightness targets in extreme climates.

### Material Durability
- Freeze-thaw regions: materials must demonstrate freeze-thaw resistance per applicable ASTM tests
- High-UV regions: membrane surfaces must meet UV stability requirements
- Marine environments: fasteners and flashings must be corrosion-resistant (stainless steel or equivalent)

### Wind Uplift
High-wind regions trigger enhanced securement requirements. Specification fastener spacing, adhesive application rates, and edge securement details vary by wind exposure category.

## Recording Climate Context

When a specification requirement is climate-dependent, the kernel records:

1. `climate_context` field with the applicable climate zone or exposure flag
2. The performance criterion value specific to that climate context
3. Source pointer to the spec clause establishing the climate dependency
4. `ambiguity_flag: true` if climate applicability is unclear

## Climate Context Is Metadata

Climate context is metadata on a specification requirement, not a separate entity. The kernel does not model climate — it records that a specification requirement varies by climate condition.
