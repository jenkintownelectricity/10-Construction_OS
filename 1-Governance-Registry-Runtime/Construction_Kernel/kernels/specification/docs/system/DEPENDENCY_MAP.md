# Dependency Map — Construction Specification Kernel

## Upstream Dependencies

This kernel depends on shared artifacts maintained in `Construction_Reference_Intelligence/shared/`. These artifacts provide canonical registries, enums, and taxonomy definitions that this kernel's schemas reference.

### Shared Artifact Dependencies

| Artifact | Path | Dependency Type | Usage |
|---|---|---|---|
| Control Layers | `shared/control_layers.json` | enum source | `control_layers_served` field values |
| Interface Zones | `shared/interface_zones.json` | enum source | `interface_zones` field values |
| Enum Registry | `shared/shared_enum_registry.json` | enum source | lifecycle_stages, climate_exposure_flags, geometry_contexts, evidence_types, confidence_levels, risk_levels, revision_postures |
| Standards Registry | `shared/shared_standards_registry.json` | reference source | Standards citation validation |
| Taxonomy | `shared/shared_taxonomy.json` | field definitions | CSI section codes, spec families, subfamilies, control functions |
| Division 07 Posture | `shared/division_07_posture.json` | domain context | Division 07 domain alignment |
| Family Context | `shared/FAMILY_CONTEXT.md` | governance | Family architecture rules |

### Pointer File

`shared/SHARED_ARTIFACTS_POINTER.md` documents the canonical source path for all shared artifacts.

## Downstream Consumers

### Construction_Reference_Intelligence

The intelligence layer reads specification truth from this kernel via `kernel_refs`. It consumes:
- Requirement records for pattern analysis
- Ambiguity flags for gap identification
- Interface zone coverage for risk assessment
- Standards references for correlation analysis
- Revision lineage for change tracking

### Sibling Kernels

Sibling kernels (Assembly, Material, Chemistry, Scope) may reference specification facts via pointer. They do not read directly from this kernel's data files — they reference specification record IDs in their own records.

## Registry

This kernel is registered in `ValidKernel_Registry` with:
- kernel_id: `KERN-CONST-SPEC`
- role: `specification-kernel`
- family: `construction-kernel`
- status: `initialized`

## Dependency Rules

1. Shared artifacts are never duplicated into this kernel
2. Shared artifact updates require baseline re-evaluation
3. This kernel never writes to shared artifacts
4. Cross-kernel references use ID pointers only
5. The intelligence layer reads from this kernel; this kernel does not read from the intelligence layer
