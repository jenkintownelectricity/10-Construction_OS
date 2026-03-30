# Family Shared Pointer

## Purpose

Points to shared family artifacts that the Scope Kernel depends on but does not own. These artifacts are maintained in the Construction Reference Intelligence repository.

## Family

**construction-kernel** family, registered in ValidKernel_Registry.

## Shared Artifact Locations

| Artifact | Canonical Path | Owner |
|---|---|---|
| Family Context | `Construction_Reference_Intelligence/shared/FAMILY_CONTEXT.md` | Reference Intelligence |
| Control Layers Registry | `Construction_Reference_Intelligence/shared/control_layers.json` | Reference Intelligence |
| Interface Zones Registry | `Construction_Reference_Intelligence/shared/interface_zones.json` | Reference Intelligence |
| Division 07 Posture | `Construction_Reference_Intelligence/shared/division_07_posture.json` | Reference Intelligence |

## Consumption Rules

1. **Read-only access.** The Scope Kernel never writes to shared artifacts.
2. **Reference by ID.** Scope records reference control layers and interface zones by their IDs from the shared registries.
3. **Validate on load.** When the kernel initializes, it validates that referenced IDs exist in the shared registries.
4. **No local copies.** Shared artifacts are never duplicated into this repository. Always reference the canonical source.

## Sibling Kernels in Family

| Kernel | Repository | Domain |
|---|---|---|
| Scope Kernel | `Construction_Scope_Kernel` | Scope of work, trade coordination |
| Spec Kernel | `Construction_Specification_Kernel` | Material and product specifications |
| Assembly Kernel | `Construction_Assembly_Kernel` | Assembly procedures and details |
| Material Kernel | `Construction_Material_Kernel` | Material properties |
| Chemistry Kernel | `Construction_Chemistry_Kernel` | Chemical behavior and compatibility |

## Update Protocol

When shared artifacts are updated in Reference Intelligence:
1. All sibling kernels are notified.
2. Each kernel validates its references against the updated registry.
3. Broken references are flagged as scope gaps.
4. Resolution requires human review of affected scope records.
