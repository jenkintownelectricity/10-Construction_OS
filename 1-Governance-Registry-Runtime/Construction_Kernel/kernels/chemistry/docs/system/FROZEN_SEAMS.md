# Frozen Seams

## Purpose

Documents the stable interface contracts between the Chemistry Kernel and its sibling kernels. Frozen seams are interfaces that have been agreed upon and must not change without coordinated versioning across all affected kernels.

## Frozen Seam: Chemistry → Material Kernel

| Aspect | Contract |
|---|---|
| **Direction** | Chemistry publishes; Material references |
| **Reference mechanism** | Material records contain `chemistry_ref` pointing to a Chemical System ID (`CSYS-xxx`) |
| **Chemistry does not import** | Tensile, elongation, hardness, density, dimensions |
| **Material does not import** | Cure mechanisms, adhesion rules, incompatibility rules |
| **Frozen since** | v0.1 |

## Frozen Seam: Chemistry → Assembly Kernel

| Aspect | Contract |
|---|---|
| **Direction** | Chemistry publishes; Assembly consumes |
| **Reference mechanism** | Assembly records reference chemistry via adhesion rules and incompatibility rules |
| **Chemistry provides** | Cure conditions, adhesion requirements, compatibility constraints |
| **Chemistry does not provide** | Installation sequences, application methods, layer order |
| **Frozen since** | v0.1 |

## Frozen Seam: Chemistry → Specification Kernel

| Aspect | Contract |
|---|---|
| **Direction** | Chemistry publishes; Specification references |
| **Reference mechanism** | Specification sections may reference chemistry families and compatibility rules |
| **Chemistry does not provide** | Product approvals, submittal requirements, compliance determinations |
| **Frozen since** | v0.1 |

## Frozen Seam: Chemistry → Reference Intelligence

| Aspect | Contract |
|---|---|
| **Direction** | Chemistry publishes; Intelligence consumes and synthesizes |
| **Reference mechanism** | Intelligence layer queries chemistry records by typed ID |
| **Contract** | Intelligence must respect status flags, evidence tiers, and fail-closed posture |
| **Intelligence may not** | Modify chemistry records or create chemistry truth |
| **Frozen since** | v0.1 |

## Seam Modification Protocol

Any change to a frozen seam requires:
1. Proposal documented in both affected kernels
2. Schema version increment in both kernels
3. Migration path for existing records
4. Coordinated deployment
