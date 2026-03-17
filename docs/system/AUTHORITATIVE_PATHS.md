# Authoritative Paths — Construction_Application_OS

## First-Read Priority Order

1. `README.md` — Repo purpose, stack position, responsibilities
2. `os/CONSTRUCTION_APPLICATION_OS_V0.1.md` — OS identity and app definitions
3. `docs/system/REPO_MANIFEST.md` — Ownership and boundaries
4. `docs/system/FROZEN_SEAMS.md` — Frozen surfaces
5. `maps/stack_map.md` — Full stack context

## Authoritative Files

| File | Authority |
|------|-----------|
| `os/CONSTRUCTION_APPLICATION_OS_V0.1.md` | Defines OS identity, apps, workflows, roles |
| `os/app_inventory.md` | Canonical app list |
| `maps/app_to_runtime_map.md` | App-to-runtime capability mappings |
| `maps/app_to_kernel_map.md` | App-to-kernel domain mappings |
| `maps/stack_map.md` | Stack layer definitions |

## Supporting Files

| File | Role |
|------|------|
| `apps/*/README.md` | Per-app overviews |
| `apps/*/workflow.md` | Per-app workflow details |
| `apps/*/dependencies.md` | Per-app dependency lists |
| `workflows/*.md` | Cross-cutting workflow definitions |
| `os/role_model.md` | Role definitions |
| `os/workflow_inventory.md` | Workflow catalog |

## Paths to Skip Unless Explicitly Needed
- `ui/` — Conceptual only in v0.1; skip unless working on UI design

## Paths Reserved for Audit/Debug/Deep Work
- `apps/*/inputs.md` — Input contract details
- `apps/*/outputs.md` — Output contract details
