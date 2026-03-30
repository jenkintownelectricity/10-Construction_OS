# Kernel-to-Family Map

## Purpose

Describes how the Construction Chemistry Kernel fits within the broader construction-kernel family.

## Position in Family

The Construction Chemistry Kernel is a domain-specific kernel within the ValidKernel registry. It provides chemistry truth data consumed by sibling kernels and upstream systems.

## Sibling Kernels

| Kernel | Relationship |
|---|---|
| Construction_Material_Kernel | Chemistry kernel provides compatibility and cure data for materials defined in the material kernel. `material_refs` in chemical systems point to material entries. |
| Construction_Spec_Kernel | Specification sections reference chemistry constraints (VOC limits, cure requirements, adhesion rules). |
| Construction_Inspection_Kernel | Inspection checklists consume adhesion rules and incompatibility rules to verify field conditions. |
| Construction_Assembly_Kernel | Assembly definitions reference chemical systems for sealant joints, adhesive bonds, and coatings. |

## Data Flow Direction

- Chemistry kernel is a **source** kernel. It publishes truth records.
- Sibling kernels **consume** chemistry data via string references (e.g., `chemistry_ref`, `cure_mechanism_ref`).
- No chemistry record embeds data from other kernels. Cross-kernel references are IDs only.

## Shared Artifacts

- Schema version convention (`v1`) is shared across the family.
- Status enum (`active`, `draft`, `deprecated`) is consistent across all kernels.
- Evidence reference format is shared with inspection and material kernels.

## Governance

- Chemistry kernel schema changes are versioned independently.
- Breaking changes to referenced IDs require coordination with consuming kernels.
- Deprecated records are retained for traceability; they are never deleted.
