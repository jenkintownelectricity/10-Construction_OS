# Family Dependency Posture

## Purpose

Documents the Construction Chemistry Kernel's dependencies on shared artifacts and sibling kernels.

## Dependency Classification

| Dependency | Type | Direction | Description |
|---|---|---|---|
| Construction_Material_Kernel | Sibling kernel | Outbound | Chemical systems reference materials via `material_refs`. Chemistry kernel does not import material data. |
| Construction_Spec_Kernel | Sibling kernel | Consumed by | Specifications reference chemistry constraints. Chemistry kernel is unaware of spec records. |
| Construction_Inspection_Kernel | Sibling kernel | Consumed by | Inspections consume adhesion rules, incompatibility rules, and cure constraints. |
| Construction_Assembly_Kernel | Sibling kernel | Consumed by | Assemblies reference chemical systems for joints, bonds, and coatings. |
| ValidKernel Registry | Parent registry | Registered in | Chemistry kernel is registered as a domain kernel in the ValidKernel family. |

## Shared Artifacts

- **Schema version convention:** `v1` string constant, shared across all kernels.
- **Status enum:** `active`, `draft`, `deprecated` — consistent across the family.
- **Evidence reference format:** String IDs prefixed by type (e.g., `EVD-LAB-`, `EVD-FIELD-`, `EVD-MFR-`).
- **ID prefix conventions:** `CHEM-SYS-`, `CURE-`, `ADH-`, `INCOMPAT-`, `DEG-`, `HAZ-`.

## Independence Guarantees

- Chemistry kernel has **no hard runtime dependencies** on any sibling kernel.
- All cross-kernel references are string IDs. Missing targets do not break schema validation.
- Chemistry kernel can be validated, tested, and deployed independently.

## Coordination Requirements

- Renaming or retiring a `system_id` requires notification to consuming kernels.
- New chemistry families added to the enum should be communicated to the material kernel.
- Evidence reference format changes require family-wide coordination.

## Risk Posture

- **Low coupling:** String-only references, no embedded foreign data.
- **High cohesion:** All entities serve the chemistry domain exclusively.
- **No circular dependencies:** Chemistry kernel is a source; it does not consume sibling kernel data.
