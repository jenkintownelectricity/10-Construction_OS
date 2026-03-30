# Climate Posture — Construction Assembly Kernel

## Principle

Climate affects assembly configuration. The position of vapor retarders, the type and thickness of insulation, drainage requirements, and material selection all vary by climate zone and exposure conditions. The kernel records climate context as metadata — it does not contain climate models or perform hygrothermal analysis.

## Climate-Driven Assembly Decisions

### Vapor Retarder Position

The position of the vapor control layer within an assembly is climate-dependent:

- **Cold climates (ASHRAE zones 5-8)**: Vapor retarder positioned on the warm (interior) side of insulation to prevent warm moist air from reaching cold surfaces.
- **Hot-humid climates (ASHRAE zones 1A-3A)**: Vapor retarder may be positioned on the exterior side, or omitted, depending on cooling-dominated moisture drive.
- **Mixed climates (ASHRAE zone 4A)**: Vapor retarder position requires hygrothermal analysis. Smart vapor retarders (variable permeance) may be specified.

The kernel records vapor retarder position in the layer stack and notes the climate basis in `climate_context`.

### Insulation Strategy

- **Cold climates**: Higher R-values per ASHRAE 90.1 Table 5.5. Continuous insulation outboard of structure to minimize thermal bridging.
- **Hot climates**: Reflective surfaces and above-deck insulation for roof assemblies. Cool roof requirements.
- **Freeze-thaw zones**: Insulation must be closed-cell or moisture-tolerant below grade and at exposed edges.

### Drainage Requirements

- **High precipitation zones**: Enhanced drainage plane design. Rainscreen wall assemblies with defined drainage cavities.
- **Severe precipitation**: Redundant water control layers. Primary and secondary drainage.

### Wind Exposure

- **High wind zones**: Mechanically attached or fully adhered membrane systems. Enhanced edge securement per SPRI ES-1. Higher wind uplift ratings per FM 4470.
- **Coastal exposure**: Corrosion-resistant fasteners and edge metals. Salt spray resistance.

## Climate Context in Kernel Objects

### assembly_system.climate_context

Records the climate conditions the assembly is designed for:

```json
{
  "climate_zone": "5A",
  "exposure_flags": ["freeze_thaw", "high_wind"],
  "exposure_class": "severe"
}
```

### Enum Values

From `shared_enum_registry.json#climate_exposure_flags`:
- marine_exposure, high_uv, freeze_thaw, coastal_salt, high_wind, high_humidity, severe_precipitation

From `shared_taxonomy.json#exposure_class`:
- sheltered, moderate, severe, extreme

## Limitations

- The kernel records climate context; it does not perform hygrothermal simulation.
- Dew-point calculations, condensation risk analysis, and moisture modeling are outside kernel scope.
- Climate-driven material selection decisions reference the Material Kernel.
- Climate pattern intelligence (regional failure trends, climate-correlated defects) belongs to the Reference Intelligence layer.
