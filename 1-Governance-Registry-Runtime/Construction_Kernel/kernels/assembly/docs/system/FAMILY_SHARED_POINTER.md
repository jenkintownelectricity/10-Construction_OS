# Family Shared Pointer — Construction Assembly Kernel

## Family Membership

This kernel is a member of the **construction-kernel** family, registered in ValidKernel_Registry.

## Shared Artifact Source

All shared family artifacts are maintained in the reference intelligence layer:

- **Source repository**: Construction_Reference_Intelligence
- **Shared artifacts directory**: `shared/`

## Canonical Shared Artifacts

| Artifact | Path | Description |
|---|---|---|
| Family Context | `shared/FAMILY_CONTEXT.md` | Family architecture, kernel roles, coordination rules |
| Control Layer Registry | `shared/control_layers.json` | 11 control-layer definitions with IDs and descriptions |
| Interface Zone Registry | `shared/interface_zones.json` | 10 interface zone definitions with IDs and descriptions |
| Division 07 Posture | `shared/division_07_posture.json` | CSI Division 07 domain posture and subsection listing |
| Shared Enum Registry | `shared/shared_enum_registry.json` | Canonical enum values for lifecycle, climate, geometry, risk, confidence |
| Shared Standards Registry | `shared/shared_standards_registry.json` | Standards reference definitions (IBC, NFPA, ASHRAE, ASTM, etc.) |
| Shared Evidence Registry | `shared/shared_evidence_registry.json` | Evidence type classifications and quality tiers |
| Shared Risk Registry | `shared/shared_risk_registry.json` | Risk categories, severity levels, and assessment posture |
| Shared Taxonomy | `shared/shared_taxonomy.json` | Shared taxonomy field definitions and allowed values |

## Non-Duplication Rule

This kernel MUST NOT duplicate shared artifacts. It references them by pointer using the paths above. If a shared value is needed in a schema, the schema references the shared registry by description or documentation — it does not embed the shared file.

## Local Pointer File

This kernel's local pointer to shared artifacts: `shared/SHARED_ARTIFACTS_POINTER.md`

## Sibling Kernels

All siblings consume the same shared artifacts:

| Kernel | Role |
|---|---|
| Construction_Specification_Kernel | Specification truth |
| Construction_Material_Kernel | Material truth |
| Construction_Chemistry_Kernel | Chemistry truth |
| Construction_Scope_Kernel | Scope truth |
| Construction_Assembly_Kernel | Assembly truth (this kernel) |
