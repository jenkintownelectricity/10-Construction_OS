# Climate Context Model — Construction Material Kernel

## Purpose

Climate conditions affect material performance, degradation rates, and selection constraints. This model defines how climate context is attached to material records as metadata.

## Climate Parameters

| Parameter | Unit | Material Relevance |
|---|---|---|
| Temperature range | deg F | Thermal expansion, brittleness, softening |
| UV radiation index | kLy/year | Polymer degradation rate |
| Annual precipitation | inches | Moisture exposure frequency |
| Relative humidity (sustained) | % RH | Vapor drive, moisture absorption |
| Freeze-thaw cycles | cycles/year | Dimensional cycling, adhesion stress |
| Wind speed (design) | mph | Mechanical stress on membranes |
| Salt spray exposure | binary | Coastal corrosion and chemical attack |

## Climate Zone References

Material records reference climate zones from ASHRAE 169 or IECC classifications:

| Zone | Description | Key Material Concerns |
|---|---|---|
| 1A-2A | Hot-Humid | UV exposure, high vapor drive inward |
| 3A-4A | Mixed-Humid | Seasonal vapor drive reversal |
| 5A-6A | Cold-Humid | Freeze-thaw, condensation risk |
| 7-8 | Very Cold/Subarctic | Extreme cold brittleness, ice damming |
| 3B-4B | Mixed-Dry | UV exposure, thermal cycling |
| 5B-6B | Cold-Dry | Freeze-thaw, low humidity |
| 3C | Marine | Moderate temperature, sustained moisture |

## Climate Context in Records

The optional `climate_context` field in performance and weathering records may include:

- **climate_zone** — ASHRAE zone identifier (e.g., "4A")
- **exposure_severity** — mild, moderate, severe
- **key_stressor** — primary climate factor affecting the property
- **applicability_note** — how climate affects property interpretation

## Climate-Dependent Material Properties

| Property | Climate Sensitivity | Example |
|---|---|---|
| Vapor permeance | Temperature and RH dependent | Permeance increases with temperature |
| R-value | Temperature dependent | Polyiso R-value decreases below 40 deg F |
| Elongation | Temperature dependent | Elastomers stiffen in cold |
| Adhesion | Application temperature bounded | Many adhesives require 40 deg F minimum |
| UV resistance | Latitude and altitude dependent | Higher UV at elevation |

## Rules

1. Climate context is metadata — it does not change the property value itself
2. Climate-dependent property values must state the conditions under which they were measured
3. The kernel does not recommend materials for specific climate zones
4. Climate zone classifications come from the shared registry
5. Climate modeling and simulation are outside kernel scope
