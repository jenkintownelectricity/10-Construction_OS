# Family Dependency Posture — Construction Specification Kernel

## Dependency Direction

This kernel depends on shared artifacts from the construction-kernel family. It does not create dependencies that other kernels must satisfy before they can function.

## Shared Artifact Dependencies

### Required for Schema Validation
- `shared/control_layers.json` — enum values for control_layers_served and control_layers fields
- `shared/interface_zones.json` — enum values for interface_zones field
- `shared/shared_enum_registry.json` — enum values for lifecycle_stage, climate exposure flags, geometry contexts

### Required for Standards Reference Validation
- `shared/shared_standards_registry.json` — reference IDs for standards citations

### Required for Taxonomy Alignment
- `shared/shared_taxonomy.json` — field definitions for CSI section codes, spec families, subfamilies

### Required for Domain Context
- `shared/division_07_posture.json` — Division 07 domain alignment

### Required for Governance
- `shared/FAMILY_CONTEXT.md` — family architecture and coordination rules

## Dependency Health

| Dependency | Type | Impact if Missing |
|---|---|---|
| control_layers.json | enum source | Cannot validate control layer references |
| interface_zones.json | enum source | Cannot validate interface zone references |
| shared_enum_registry.json | enum source | Cannot validate lifecycle, climate, geometry fields |
| shared_standards_registry.json | reference source | Cannot validate standards citations |
| shared_taxonomy.json | field definitions | Cannot validate taxonomy fields |

## Dependency Management Rules

1. Shared artifacts are consumed by pointer, never duplicated
2. If a shared artifact is unavailable, kernel validation fails closed (rejects records)
3. Shared artifact updates trigger baseline re-evaluation
4. This kernel never modifies shared artifacts
5. Shared artifact version compatibility is tracked in FROZEN_SEAMS.md

## No Circular Dependencies

This kernel reads from shared artifacts. The intelligence layer reads from this kernel. No circular dependency exists. The intelligence layer maintains shared artifacts independently of this kernel's consumption.
