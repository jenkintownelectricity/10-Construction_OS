# Kernel-to-Digital-Twin Map — Construction Material Kernel

## Status: Stub

No digital twin integration currently exists. This map will be populated when digital twin systems are implemented.

## Planned Digital Twin Data Contributions

| Material Data | Digital Twin Use | Status |
|---|---|---|
| Material properties | Populate material attributes in twin model | Not implemented |
| Weathering behavior | Feed degradation models for aging simulation | Not implemented |
| Hygrothermal properties | Support moisture transport modeling | Not implemented |
| Compatibility data | Validate material adjacency in twin | Not implemented |
| Lifecycle context | Track material condition over building life | Not implemented |

## Design Constraints

1. Digital twin reads material data from frozen seam contracts
2. Material kernel provides static property truth; twin owns temporal state
3. Twin-generated predictions are not written back to material kernel
4. Material kernel provides initial and aged property values; twin interpolates
