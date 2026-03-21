# Construction OS Registry

Canonical platform inventory and topology authority for the Construction OS architecture.

This registry catalogs all repositories that are confirmed members of the Construction OS platform, their layer assignments, and their architectural roles.

## Construction OS Core Architecture (FROZEN)

```
Universal_Truth_Kernel
├── ValidKernel_Geometry_Kernel
├── ValidKernel-Governance
└── Construction_Kernel
     ├── Construction_Atlas (formerly Construction_Atlas_UI)
     │        ↓
     Construction_Runtime
              ↓
     Construction_Application_OS

Infrastructure Authorities:
  Construction_OS_Registry              ← YOU ARE HERE (Construction OS topology authority)
  ValidKernel_Registry                  → Global kernel lineage authority
  ValidKernelOS_VKBUS                   → Canonical interaction transport layer
```

> **Architecture Status:** FROZEN
> **Atlas Status:** Core spatial construction context layer
> **UI Authority:** Construction_Application_OS is the sole UI surface of Construction OS.
> **Rename Lineage:** Construction_Atlas_UI → Construction_Atlas (V2) — separation of spatial context truth layer and UI surface. This lineage reference is permanent.

## Platform Inventory

See `registry/platform_inventory.json` for the machine-readable canonical inventory.

## Layer Map

For the canonical Construction OS layer map, see [`Construction_Kernel/docs/system/CONSTRUCTION_OS_LAYER_MAP.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_OS_LAYER_MAP.md).

## Scope

This registry covers only repositories that have been confirmed as part of the Construction OS platform through architectural audit. Systems classified as PRE-UTK or independent are explicitly excluded.

## Registry Rules

- Entries are documentation-only and do not affect runtime behavior
- All entries must be confirmed through architectural audit before inclusion
- PRE-UTK systems must NOT be listed in this registry
- Layer and primary_area fields must align with confirmed audit findings

---

## Architecture References

- **Construction Truth Spine**: See [`Construction_Kernel/docs/system/CONSTRUCTION_TRUTH_SPINE.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_TRUTH_SPINE.md) for the canonical truth history architecture.
- **Construction Assembly Identity System**: See [`Construction_Kernel/docs/system/CONSTRUCTION_ASSEMBLY_IDENTITY_SYSTEM.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_ASSEMBLY_IDENTITY_SYSTEM.md) for governed object identity architecture.
- **Construction Object Evidence and Matching**: See [`Construction_Kernel/docs/system/CONSTRUCTION_OBJECT_EVIDENCE_AND_MATCHING.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_OBJECT_EVIDENCE_AND_MATCHING.md) for evidence and matching basis architecture.
- **Construction Assembly Composition Model**: See [`Construction_Kernel/docs/system/CONSTRUCTION_ASSEMBLY_COMPOSITION_MODEL.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_ASSEMBLY_COMPOSITION_MODEL.md) for canonical assembly composition architecture.
- **Construction Assembly Graph**: See [`Construction_Kernel/docs/system/CONSTRUCTION_ASSEMBLY_GRAPH.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_ASSEMBLY_GRAPH.md) for assembly graph representation.
- **Construction Interface and Adjacent Systems Model**: See [`Construction_Kernel/docs/system/CONSTRUCTION_INTERFACE_AND_ADJACENT_SYSTEMS_MODEL.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_INTERFACE_AND_ADJACENT_SYSTEMS_MODEL.md) for interface and adjacent systems architecture.
- **Construction Scope Boundary Model**: See [`Construction_Kernel/docs/system/CONSTRUCTION_SCOPE_BOUNDARY_MODEL.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_SCOPE_BOUNDARY_MODEL.md) for scope boundary and coordination obligation architecture.
- **Construction Material Taxonomy**: See [`Construction_Kernel/docs/system/CONSTRUCTION_MATERIAL_TAXONOMY.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_MATERIAL_TAXONOMY.md) for canonical material class vocabulary.
- **Construction Material Compatibility Model**: See [`Construction_Kernel/docs/system/CONSTRUCTION_MATERIAL_COMPATIBILITY_MODEL.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_MATERIAL_COMPATIBILITY_MODEL.md) for material compatibility rules.
- **Construction View Intent Model**: See [`Construction_Kernel/docs/system/CONSTRUCTION_VIEW_INTENT_MODEL.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_VIEW_INTENT_MODEL.md) for view intent architecture.
- **Construction Detail Applicability Model**: See [`Construction_Kernel/docs/system/CONSTRUCTION_DETAIL_APPLICABILITY_MODEL.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_DETAIL_APPLICABILITY_MODEL.md) for detail selection architecture.
- **Construction Detail Schema**: See [`Construction_Kernel/docs/system/CONSTRUCTION_DETAIL_SCHEMA.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/CONSTRUCTION_DETAIL_SCHEMA.md) for canonical detail logic representation.
- **Drawing Instruction IR**: See [`Construction_Kernel/docs/system/DRAWING_INSTRUCTION_IR.md`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/docs/system/DRAWING_INSTRUCTION_IR.md) for engine-agnostic drawing instruction layer.
- **Deterministic Drawing Runtime**: See [`Construction_Runtime/docs/system/DETERMINISTIC_DRAWING_RUNTIME.md`](https://github.com/jenkintownelectricity/Construction_Runtime/blob/master/docs/system/DETERMINISTIC_DRAWING_RUNTIME.md) for runtime execution engine architecture.
- **Kernel/Runtime Contract Seams**: See [`Construction_Kernel/contracts/seams/seam_manifest.json`](https://github.com/jenkintownelectricity/Construction_Kernel/blob/master/contracts/seams/seam_manifest.json) for governed contract seam definitions.
- **Intake & Review Surfaces**: See [`Construction_Runtime/docs/system/INTAKE_APPLICATION_SURFACES.md`](https://github.com/jenkintownelectricity/Construction_Runtime/blob/master/docs/system/INTAKE_APPLICATION_SURFACES.md) for Wave 7 intake application architecture.

---

## Repository Rename Notice

This repository was originally created under the name `ConstructionOS_Registry`.

It was renamed to `Construction_OS_Registry` to align with the canonical naming conventions used across the Construction OS ecosystem.

This rename does not represent an architectural change.

No lineage relationships, registry structures, or classifications were modified.

Only the repository identifier was corrected.
