# Weathering Model — Construction Material Kernel

## Purpose

This model defines how material degradation under environmental exposure is recorded. Weathering behavior captures how materials respond to UV radiation, thermal cycling, moisture, freeze-thaw, chemical exposure, and biological attack.

## Weathering Record Structure

| Field | Type | Required | Description |
|---|---|---|---|
| behavior_id | string | Yes | Unique identifier |
| material_ref | string | Yes | ID of the material |
| exposure_type | enum | Yes | uv, thermal_cycling, moisture, freeze_thaw, chemical, biological |
| degradation_rate | string | Yes | Published degradation rate or severity |
| status | enum | Yes | active, draft, deprecated |
| test_method_ref | string | No | Reference to weathering test standard |
| service_life_impact | string | No | Published effect on service life |
| climate_context | object | No | Climate zone or exposure conditions |
| notes | string | No | Additional context |

## Exposure Types

### UV Exposure
Polymer degradation from ultraviolet radiation. Affects surface integrity, color stability, elongation, and tensile strength. Tested per ASTM G154 (QUV), ASTM G155 (xenon arc), or natural outdoor exposure studies.

### Thermal Cycling
Repeated expansion and contraction from temperature changes. Affects dimensional stability, seam integrity, and adhesion. Critical for roofing membranes experiencing daily and seasonal temperature swings.

### Moisture Exposure
Sustained or cyclic water contact. Affects moisture absorption, R-value retention (insulation), adhesion, and biological growth potential. Includes rain, condensation, and ponding water.

### Freeze-Thaw Cycling
Repeated freezing and thawing of absorbed moisture. Affects dimensional stability, surface integrity, and compressive strength. Critical in ASHRAE climate zones 5 through 8.

### Chemical Exposure
Contact with chemicals in the service environment. Includes acid rain, industrial pollutants, cleaning agents, and adjacent material leachates. Varies by location and building use.

### Biological Exposure
Fungal, algal, or microbial growth on material surfaces. Affects appearance, surface integrity, and may indicate moisture retention problems.

## Degradation Rate Expression

Degradation rates are recorded as published. Common formats:
- Percent property retention after stated exposure duration
- Visual rating scale (e.g., ASTM D660 for cracking)
- Pass/fail against minimum threshold after exposure
- Qualitative severity (low, moderate, high) from published studies

## Weathering Data Rules

1. Accelerated weathering results must state the acceleration protocol and duration
2. Natural weathering results must state exposure location and duration
3. The kernel does not extrapolate weathering data beyond tested durations
4. Synergistic effects (UV + moisture simultaneously) are recorded only if specifically tested
5. Weathering records link to the Chemistry Kernel for degradation mechanism explanations
