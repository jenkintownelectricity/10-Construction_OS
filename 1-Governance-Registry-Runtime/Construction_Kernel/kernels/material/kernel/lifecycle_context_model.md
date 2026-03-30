# Lifecycle Context Model — Construction Material Kernel

## Purpose

Material properties change over a material's service life due to aging, environmental exposure, and loading history. This model defines how lifecycle context is recorded alongside material property data.

## Lifecycle Stages

| Stage | Description | Typical Evidence Source |
|---|---|---|
| as_manufactured | Properties at time of manufacture | Manufacturer TDS, factory QC tests |
| post_installation | Properties measured after field installation | Field test reports |
| in_service_early | Properties within first 5 years of service | Field monitoring studies |
| in_service_aged | Properties after extended service (5+ years) | Aged-material testing, core samples |
| post_exposure_event | Properties after specific event (hail, fire, flood) | Forensic analysis reports |
| end_of_service | Properties at removal or replacement | Core sample testing |

## Lifecycle Data in Property Records

Material property records may include lifecycle context through:

- **conditions** field — describes the lifecycle state of the material when tested
- **evidence_ref** — points to the evidence source documenting the aged condition
- **notes** — additional lifecycle context

## Known Lifecycle Effects for Division 07 Materials

| Material Class | Key Lifecycle Effect | Property Affected |
|---|---|---|
| Thermoplastic (TPO) | UV degradation of surface | Elongation, flexibility |
| Thermoset (EPDM) | Plasticizer loss over time | Hardness, elongation |
| Bituminous | Oxidative hardening | Flexibility, adhesion |
| Cellular plastic (polyiso) | Long-term thermal drift | R-value per inch |
| Mineral fiber | Moisture absorption over time | R-value, density |
| Elastomer (sealants) | UV and ozone degradation | Elongation, adhesion |
| Fluid applied | Film thickness reduction | Permeance, crack bridging |

## Lifecycle Data Rules

1. Lifecycle-stage property data requires the same evidence rigor as initial data
2. Aged-material test results must reference the aging duration and conditions
3. Accelerated aging data is tagged with the acceleration protocol (xenon arc, QUV, heat aging)
4. The kernel does not extrapolate from accelerated data to real-time aging
5. Multiple lifecycle-stage records for the same property are permitted — each is a distinct truth record

## Lifecycle Data Gaps

When lifecycle data is expected but unavailable (e.g., no long-term EPDM elongation data), the gap is not filled with estimates. The absence of a lifecycle-stage property record indicates a data gap. The intelligence layer may surface these gaps for industry research.

## Coordination

- Assembly Kernel uses lifecycle data for system durability context
- Chemistry Kernel explains degradation mechanisms
- Specification Kernel may set lifecycle performance thresholds
- Intelligence layer correlates lifecycle patterns across material classes
