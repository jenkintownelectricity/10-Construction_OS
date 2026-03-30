# Dependency Map

## Purpose

Documents all dependencies between the Scope Kernel and other repositories, registries, and shared artifacts.

## Upstream Dependencies (Scope Kernel Consumes)

| Source | Artifact | Dependency Type | Required |
|---|---|---|---|
| Reference Intelligence | `shared/control_layers.json` | Shared registry | Yes |
| Reference Intelligence | `shared/interface_zones.json` | Shared registry | Yes |
| Reference Intelligence | `shared/division_07_posture.json` | Domain context | Yes |
| Reference Intelligence | `shared/FAMILY_CONTEXT.md` | Family architecture | Yes |
| ValidKernel_Registry | Kernel registration record | Governance | Yes |

## Downstream Dependencies (Other Systems Consume Scope Kernel)

| Consumer | Artifact Consumed | Dependency Type |
|---|---|---|
| Spec Kernel | Scope IDs via `scope_ref` | Cross-kernel reference |
| Assembly Kernel | Scope IDs, sequence data | Cross-kernel reference |
| Runtime systems | All scope JSON records | Operational data |
| Digital twin systems | Scope + inspection + commissioning | Monitoring data |
| AI assistants | All scope schemas and records | Query interface |

## Sibling Dependencies (Peer Kernels)

| Sibling Kernel | Relationship | Integration Point |
|---|---|---|
| Spec Kernel | Scope references specs | `spec_ref` fields |
| Assembly Kernel | Scope sequences assemblies | `assembly_ref` fields |
| Material Kernel | Scope identifies materials | `material_ref` fields |
| Chemistry Kernel | No direct dependency | None |

## Internal Dependencies

| Artifact | Depends On | Relationship |
|---|---|---|
| Work Operations | Scope of Work | `scope_ref` |
| Sequence Steps | Scope of Work | `scope_ref` |
| Trade Responsibilities | Scope of Work | `scope_ref` |
| Inspection Steps | Scope of Work | `scope_ref` |
| Commissioning Steps | Scope of Work | `scope_ref` |
| Closeout Requirements | Scope of Work | `scope_ref` |
| Warranty Handoff Records | Scope of Work | `scope_ref` |

## Dependency Health Rules

1. All upstream dependencies must be resolvable at kernel initialization.
2. Missing shared registries are a blocking error -- the kernel cannot operate without control layer and interface zone definitions.
3. Sibling kernel references are soft dependencies -- unresolved references are flagged but do not block scope operations.
