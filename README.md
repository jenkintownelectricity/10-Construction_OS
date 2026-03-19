# Construction OS Registry

Canonical platform inventory for the Construction OS architecture.

This registry catalogs all repositories that are confirmed members of the Construction OS platform, their layer assignments, and their architectural roles.

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

---

## Repository Rename Notice

This repository was originally created under the name `ConstructionOS_Registry`.

It was renamed to `Construction_OS_Registry` to align with the canonical naming conventions used across the Construction OS ecosystem.

This rename does not represent an architectural change.

No lineage relationships, registry structures, or classifications were modified.

Only the repository identifier was corrected.
