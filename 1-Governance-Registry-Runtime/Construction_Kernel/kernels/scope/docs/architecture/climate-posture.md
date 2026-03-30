# Climate Posture

## Purpose

Defines how the Scope Kernel accounts for climate as a factor that affects scope boundaries, sequencing constraints, and inspection requirements. The kernel does not own climate data -- it records how climate conditions constrain scope execution.

## Principle

Climate is a scope modifier, not scope truth. The Scope Kernel records climate-driven constraints on work operations, sequencing, and inspection without owning climate science or weather prediction.

## Climate-Affected Scope Elements

### 1. Work Operation Constraints
Operations may carry `weather_constraints` that define acceptable conditions for execution:
- Temperature ranges for adhesive application
- Wind speed limits for membrane installation
- Precipitation restrictions for waterproofing
- Humidity limits for coating application

### 2. Sequencing Constraints
Sequence steps may be climate-dependent:
- Seasonal work windows (e.g., roofing in northern climates)
- Cure time dependencies affected by temperature
- Freeze-thaw considerations for below-grade work

### 3. Inspection Timing
Some inspection types are climate-sensitive:
- Flood testing requires above-freezing conditions
- Air leakage testing may be affected by wind conditions
- Adhesion testing requires cured substrates

### 4. Commissioning Observations
BECx seasonal observations are explicitly climate-driven, designed to verify envelope performance across seasons.

## Climate Context in Scope Records

The `climate_context` field on scope records captures:
- Climate zone reference (IECC climate zones 1-8)
- Seasonal restrictions applicable to the scope
- Extreme weather considerations

## What the Scope Kernel Does NOT Do

- Does not predict weather conditions
- Does not determine climate zones (reference data from external sources)
- Does not calculate R-value requirements by climate zone (Spec Kernel domain)
- Does not model thermal performance (Material Kernel domain)

## Division 07 Climate Sensitivity

| Scope Category | Climate Sensitivity | Typical Constraint |
|---|---|---|
| Membrane roofing | High | Temperature, wind, precipitation |
| Waterproofing | High | Temperature, moisture in substrate |
| Air barriers | Medium | Temperature for adhesives |
| Insulation | Low | Generally weather-tolerant |
| Sheet metal | Low | Wind limits for hoisting |
| Sealants | High | Temperature, humidity, joint moisture |
| Fireproofing | Medium | Temperature for cure |
