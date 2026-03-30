# Family Shared Pointer — Construction Material Kernel

## Family Membership

This kernel belongs to the **construction-kernel** family. The family is coordinated through the Construction_Reference_Intelligence repository, which maintains shared artifacts consumed by all sibling kernels.

## Shared Artifact Source

- **Repository:** Construction_Reference_Intelligence
- **Branch:** main
- **Shared path:** `shared/`

## Shared Artifacts Consumed

| Artifact | Path in Intelligence Repo | Purpose |
|---|---|---|
| Family context | `shared/FAMILY_CONTEXT.md` | Family architecture and coordination rules |
| Enum registry | `shared/shared_enum_registry.json` | Controlled vocabulary for all enum fields |
| Taxonomy | `shared/shared_taxonomy.json` | Material class taxonomy definitions |
| Standards registry | `shared/shared_standards_registry.json` | Standards citation format and identifiers |
| Control layers | `shared/control_layers.json` | 11 building envelope control layers |
| Interface zones | `shared/interface_zones.json` | 10 building envelope interface zones |
| Division 07 posture | `shared/division_07_posture.json` | CSI Division 07 domain alignment |

## Duplication Policy

Shared artifacts are never duplicated into this repository. All references to shared values use pointers to the canonical source. If a shared artifact changes, this kernel's schemas may need validation against the updated values.

## Version Coordination

Shared artifacts are versioned at the family level. When a shared artifact version advances, all sibling kernels validate compatibility. This kernel's baseline state records the shared artifact versions it was validated against.

## Sibling Kernels

| Kernel | Repository | Owns |
|---|---|---|
| Specification | Construction_Specification_Kernel | Specification truth |
| Assembly | Construction_Assembly_Kernel | Assembly truth |
| Chemistry | Construction_Chemistry_Kernel | Chemistry truth |
| Scope | Construction_Scope_Kernel | Scope truth |
| Material (this) | Construction_Material_Kernel | Material truth |
